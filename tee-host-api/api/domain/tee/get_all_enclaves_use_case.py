from typing import Dict

import api_logger

from repository import nitro_cli_repository
from domain.tee.entities import Enclave, EnclaveState

logger = api_logger.get()


async def execute() -> Dict[str, Enclave]:
    enclaves = nitro_cli_repository.describe_enclaves()
    logger.info(f"Enclaves: {enclaves}")
    # Return a dictionary of Enclave objects with the enclave name as the key
    return {
        enclave["EnclaveName"]: Enclave(
            enclave["EnclaveName"],
            int(enclave["EnclaveCID"]),
            EnclaveState(enclave["State"].upper()),
        )
        for enclave in enclaves
    }
