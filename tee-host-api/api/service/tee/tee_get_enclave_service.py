from fastapi import HTTPException

import api_logger

from service.tee.entities import TeeGetEnclaveResponse
from domain.tee import get_all_enclaves_use_case

logger = api_logger.get()

async def execute(name: str) -> TeeGetEnclaveResponse:
    try:
        enclaves = await get_all_enclaves_use_case.execute()
        if name in enclaves:
            enclave = enclaves[name]
            return TeeGetEnclaveResponse(
                enclave_name=enclave.name,
                enclave_cid=enclave.cid,
                enclave_status=enclave.state.value,
            )
        raise HTTPException(status_code=404, detail=f"Enclave {name} not found")
    except Exception as e:
        logger.error(f"Enclave name: {name} - Error getting enclave: {str(e)}")
        raise HTTPException(status_code=500, detail=f"Error: {str(e)}")
