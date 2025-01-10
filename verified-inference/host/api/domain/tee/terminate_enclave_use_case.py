from repository import nitro_cli_repository


async def execute(name: str) -> str:
    terminate_result = nitro_cli_repository.terminate_enclave(name)
    print(f"Enclave terminated: {terminate_result}")

    return terminate_result
