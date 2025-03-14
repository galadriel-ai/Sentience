import api_logger

from typing import Dict
from repository import nitro_cli_repository

logger = api_logger.get()


async def execute(name: str) -> Dict:
    terminate_result = nitro_cli_repository.terminate_enclave(name)
    logger.info(f"Enclave terminated: {terminate_result}")
    return terminate_result
