import socket

VSOCK_PORT = 5000
GET_ATTESTATION_REQUEST = "GET_ATTESTATION_DOC"
TIMEOUT_IN_SECONDS = 5
BUFFER_SIZE = 4096


async def request_attestation(enclave_cid: int, message: str) -> str:
    vsock = socket.socket(socket.AF_VSOCK, socket.SOCK_STREAM)
    try:
        # Connect to the enclave
        vsock.connect((enclave_cid, VSOCK_PORT))

        # Send a request for the attestation document
        vsock.sendall(GET_ATTESTATION_REQUEST.encode())

        # Set a timeout for the response
        vsock.settimeout(TIMEOUT_IN_SECONDS)

        # Receive the attestation document
        response = vsock.recv(BUFFER_SIZE)

        return response.decode()
    finally:
        vsock.close()
