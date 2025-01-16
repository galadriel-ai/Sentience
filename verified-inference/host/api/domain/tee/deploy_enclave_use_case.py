from typing import Any
from typing import Dict
from repository import nitro_cli_repository


async def execute(name: str, docker_hub_image: str, env_vars: Dict[str, Any]) -> Dict:
    build_result = nitro_cli_repository.build_enclave(name, docker_hub_image)
    print(f"Enclave built: {build_result}")

    running_result = nitro_cli_repository.run_enclave(name)
    print(f"Enclave running: {running_result}")

    return running_result
