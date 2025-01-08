from fastapi import HTTPException
import socket
from service.tee.entities import TeeAttestationResponse

VSOCK_PORT = 5000
GET_ATTESTATION_REQUEST = "GET_ATTESTATION_DOC"
BUFFER_SIZE = 4096


async def execute(enclave_cid: str) -> TeeAttestationResponse:
    vsock = socket.socket(socket.AF_VSOCK, socket.SOCK_STREAM)
    try:
        # Connect to the enclave
        vsock.connect((int(enclave_cid), VSOCK_PORT))

        # Send a request for the attestation document
        vsock.sendall(GET_ATTESTATION_REQUEST.encode())

        # Receive the attestation document
        response = vsock.recv(BUFFER_SIZE)

        return response.decode()
    except Exception as e:
        raise HTTPException(status_code=503, detail=f"Error getting attestation: {str(e)}")
    finally:
        vsock.close()
