import api_logger

from repository.vsock_repository import request_attestation
from domain.tee import get_all_enclaves_use_case

logger = api_logger.get()


async def execute(enclave_name: str) -> str:
    enclaves = await get_all_enclaves_use_case.execute()
    if enclave_name not in enclaves:
        raise Exception(f"Enclave {enclave_name} not found")

    enclave = enclaves[enclave_name]
    logger.info(f"Requesting attestation from enclave: {enclave_name}")
    response = await request_attestation(enclave.cid)
    logger.info(f"Attestation response: {response}")

    return response
