import json
from typing import Dict
from repository import nitro_cli_repository
from domain.tee.entities import Enclave, EnclaveState


async def execute() -> Dict[str, Enclave]:
    enclaves = json.loads(nitro_cli_repository.describe_enclaves())
    # Return a dictionary of Enclave objects with the enclave name as the key
    return {
        enclave["EnclaveName"]: Enclave(
            enclave["EnclaveName"],
            int(enclave["EnclaveCID"]),
            EnclaveState(enclave["State"].upper()),
        )
        for enclave in enclaves
    }
