import asyncio

BUFFER_SIZE = 4096
HOST = "0.0.0.0"
PORT = 5000
VSOCK_PORT = 5000


async def forward_data(reader, writer):
    try:
        while True:
            data = await reader.read(BUFFER_SIZE)
            if not data:
                break
            writer.write(data)
            await writer.drain()
    except Exception as e:
        print(f"Error forwarding data: {e}")
    finally:
        writer.close()
        await writer.wait_closed()


async def handle_client(cid, reader, writer):
    try:
        vsock_reader, vsock_writer = await asyncio.open_connection("localhost", VSOCK_PORT)
        await asyncio.gather(forward_data(reader, vsock_writer), forward_data(vsock_reader, writer))
    except Exception as e:
        print(f"Error handling client: {e}")
    finally:
        writer.close()
        await writer.wait_closed()


async def run_proxy_service(cid: str):
    server = await asyncio.start_server(lambda r, w: handle_client(cid, r, w), HOST, PORT)

    print(f"Proxy listening on {HOST}:{PORT}, forwarding to enclave {cid} port {VSOCK_PORT}")

    async with server:
        await server.serve_forever()


# To run the proxy service
# asyncio.run(run_proxy_service('your_cid_here'))
