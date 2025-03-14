import api_logger

from domain.tee import get_all_enclaves_use_case
from repository.vsock_repository import shutdown

logger = api_logger.get()


async def execute(enclave_name: str) -> bool:
    enclaves = await get_all_enclaves_use_case.execute()
    if enclave_name not in enclaves:
        raise Exception(f"Enclave {enclave_name} not found")

    enclave = enclaves[enclave_name]
    logger.info(f"Requesting shutdown from enclave: {enclave_name}")
    shutdown_result = await shutdown(enclave.cid)
    logger.info(f"Enclave shut down: {shutdown_result}")
    return shutdown_result
