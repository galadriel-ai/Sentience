import errno
import socket
from enum import Enum
from typing import Optional

import api_logger

logger = api_logger.get()

VSOCK_PORT = 8000
TIMEOUT_IN_SECONDS = 5
BUFFER_SIZE = 8192


class VsockRequestType(Enum):
    GET_ATTESTATION = "GET_ATTESTATION_DOC"
    SHUTDOWN = "SHUTDOWN"


async def request_attestation(enclave_cid: int) -> str:
    response = _send_request(
        enclave_cid, VsockRequestType.GET_ATTESTATION, receive_response=True
    )
    if response is None:
        logger.error(f"Enclave CID: {enclave_cid} - No response received from attestation request")
        raise Exception("No response received from attestation request")
    return response


async def shutdown(enclave_cid: int) -> bool:
    try:
        response = _send_request(
            enclave_cid, VsockRequestType.SHUTDOWN, receive_response=True
        )
    except OSError as e:
        if e.errno == errno.ENOTCONN:
            # The enclave closed the connection, which is expected
            return True
        logger.error(f"Enclave CID: {enclave_cid} - Error shutting down enclave: {e}")
        return False
    if response is None:
        logger.error(f"Enclave CID: {enclave_cid} - No response received from shutdown request")
        raise Exception("No response received from shutdown request")
    return True


def _send_request(
    enclave_cid: int,
    request_type: VsockRequestType,
    receive_response: bool = False,
) -> Optional[str]:
    vsock = socket.socket(socket.AF_VSOCK, socket.SOCK_STREAM)
    try:
        # Connect to the enclave
        vsock.connect((enclave_cid, VSOCK_PORT))
        # Send the request
        vsock.sendall(request_type.value.encode())
        if receive_response:
            # Set a timeout for the response
            vsock.settimeout(TIMEOUT_IN_SECONDS)
            # Receive the response
            response = vsock.recv(BUFFER_SIZE)
            return response.decode()
        return None
    except Exception as e:
        logger.error(f"Error in vsock communication: {e}")
        raise e
    finally:
        vsock.close()
