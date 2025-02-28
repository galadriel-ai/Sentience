import asyncio
import socket
import httpx
from typing import AsyncGenerator
from fastapi import HTTPException
from fastapi import Request
from fastapi.responses import StreamingResponse

from domain.tee import get_all_enclaves_use_case

VSOCK_PORT = 8001
BUFFER_SIZE = 4096


async def execute(
    request: Request, body: bytes, enclave_name: str
) -> AsyncGenerator[str, None]:
    """
    Stream chat completions from the TEE instance.

    Args:
        enclave_name: The name of the enclave to connect to

    Yields:
        Chunks of the streaming response

    Raises:
        Exception: If the enclave is not found
        HTTPException: If the proxy request fails
    """
    enclaves = await get_all_enclaves_use_case.execute()
    if enclave_name not in enclaves:
        raise Exception(f"Enclave {enclave_name} not found")

    enclave = enclaves[enclave_name]
    async for chunk in _vsock_stream_generator(request, body, enclave.cid, VSOCK_PORT):
        yield chunk


async def _vsock_stream_generator(
    request: Request,
    body: bytes,
    cid: int,  # Context ID (CID) of the remote endpoint
    port: int,  # Port number on the remote endpoint
) -> AsyncGenerator[bytes, None]:
    """
    Generator function that streams data from a VSOCK socket.

    Args:
        request: The incoming request
        cid: The context ID of the remote endpoint
        port: The port number on the remote endpoint

    Yields:
        Chunks of data from the VSOCK socket
    """
    # Create a VSOCK socket
    sock = socket.socket(socket.AF_VSOCK, socket.SOCK_STREAM)

    try:
        # Connect to the remote endpoint
        sock.connect((cid, port))

        # Set socket to non-blocking mode for asyncio
        sock.setblocking(False)

        # Wrap it with asyncio streams
        reader, writer = await asyncio.open_connection(sock=sock)

        # Get request headers
        headers = dict(request.headers)
        request_method = request.method
        request_path = "/chat/completions"
        request_query = request.url.query
        full_path = f"{request_path}?{request_query}" if request_query else request_path

        # Build the HTTP request
        http_request = f"{request_method} {full_path} HTTP/1.1\r\n"

        # Add headers
        for name, value in headers.items():
            if name.lower() in ["host", "authorization"]:
                continue
            http_request += f"{name}: {value}\r\n"

        # Add content length if there's a body
        if body:
            http_request += f"Content-Length: {len(body)}\r\n"

        # End of headers
        http_request += "\r\n"

        # Convert to bytes and add the body
        request_bytes = http_request.encode("utf-8")
        if body:
            request_bytes += body
        # Send the request to the remote endpoint
        writer.write(request_bytes)
        await writer.drain()

        # Read the headers
        header_data = b""
        while True:
            line = await reader.readline()
            header_data += line
            if line == b"\r\n" or not line:  # Empty line indicates end of headers
                break

        # Handle chunked encoding
        while True:
            # Read the chunk size line
            chunk_size_line = await reader.readline()
            if not chunk_size_line:
                break

            # Parse the chunk size (hex string)
            try:
                chunk_size = int(chunk_size_line.strip(), 16)
            except ValueError:
                # most likely an error message from the enclave
                # yield the error message and break
                yield chunk_size_line
                break

            # A chunk size of 0 means end of response
            if chunk_size == 0:
                # Read the final CRLF
                await reader.readline()
                break

            # Read the chunk data
            chunk_data = await reader.readexactly(chunk_size)

            # Read the CRLF after the chunk
            await reader.readline()

            # Yield only the actual data
            yield chunk_data

    except Exception as e:
        print(f"Error streaming from VSOCK socket: {e}")

    finally:
        writer.close()
        await writer.wait_closed()
