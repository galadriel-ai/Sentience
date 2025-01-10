from repository import vsock_repository
from domain.tee import get_all_enclaves_use_case


async def execute(enclave_name: str) -> str:
    enclaves = await get_all_enclaves_use_case.execute()
    if enclave_name not in enclaves:
        raise Exception(f"Enclave {enclave_name} not found")

    enclave = enclaves[enclave_name]
    response = await vsock_repository.request_attestation_from_enclave(enclave.cid)

    return response
