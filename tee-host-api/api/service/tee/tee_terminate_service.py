from fastapi import HTTPException

import api_logger

from service.tee.entities import TeeTerminateResponse
from domain.tee import shutdown_enclave_use_case

logger = api_logger.get()

async def execute(
    name: str,
) -> TeeTerminateResponse:
    try:
        result = await shutdown_enclave_use_case.execute(name)
        return TeeTerminateResponse(result=result)
    except Exception as e:
        logger.error(f"Enclave name: {name} - Error terminating enclave: {str(e)}")
        raise HTTPException(
            status_code=500, detail=f"Error terminating enclave: {str(e)}"
        )
