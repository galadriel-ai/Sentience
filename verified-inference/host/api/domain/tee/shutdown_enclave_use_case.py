from domain.tee import get_all_enclaves_use_case
from repository.vsock_repository import shutdown


async def execute(enclave_name: str) -> bool:
    enclaves = await get_all_enclaves_use_case.execute()
    if enclave_name not in enclaves:
        raise Exception(f"Enclave {enclave_name} not found")

    enclave = enclaves[enclave_name]
    print(f"Requesting shutdown from enclave: {enclave_name}")
    shutdown_result = await shutdown(enclave.cid)
    print(f"Enclave shut down: {shutdown_result}")
    return shutdown_result
