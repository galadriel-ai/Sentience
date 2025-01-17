from repository.vsock_repository import request_attestation
from domain.tee import get_all_enclaves_use_case


async def execute(enclave_name: str) -> str:
    enclaves = await get_all_enclaves_use_case.execute()
    if enclave_name not in enclaves:
        raise Exception(f"Enclave {enclave_name} not found")

    enclave = enclaves[enclave_name]
    print(f"Requesting attestation from enclave: {enclave_name}")
    response = await request_attestation(enclave.cid)

    return response
