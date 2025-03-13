import asyncio
import json
import socket
from typing import Dict, Any

import api_logger

logger = api_logger.get()

ENCLAVE_ENV_VAR_RECEIVER_PORT = 3000
CONNECTION_TIMEOUT = 30.0


async def execute(enclave_cid: int, env_vars: Dict[str, Any]) -> None:
    for i in range(10):
        try:
            response = _send_env_vars(enclave_cid, env_vars)
            logger.info(
                f"Enclave CID: {enclave_cid} - Send env vars response: {response}"
            )
            return
        except socket.timeout:
            logger.error(f"Enclave CID: {enclave_cid} - Connection timed out.")
        except socket.error as e:
            logger.error(f"Enclave CID: {enclave_cid} - Socket error: {e}")
        except Exception as e:
            logger.error(f"Enclave CID: {enclave_cid} - Unexpected error: {e}")
        await asyncio.sleep(5)
        logger.warning(f"Enclave CID: {enclave_cid} - Retrying..")
    logger.error(f"Enclave CID: {enclave_cid} - Failed to send env vars")


def _send_env_vars(enclave_cid: int, env_vars: Dict[str, Any]) -> str:
    sock = socket.socket(socket.AF_VSOCK, socket.SOCK_STREAM)
    sock.settimeout(5.0)
    sock.connect((enclave_cid, ENCLAVE_ENV_VAR_RECEIVER_PORT))

    # Send the environment variables as JSON
    message = json.dumps({"env_vars": env_vars})
    sock.sendall(message.encode())

    # Receive the response
    response = sock.recv(65536)
    return response.decode()
