from fastapi import HTTPException

import api_logger

from service.tee.entities import TeeAttestationResponse
from domain.tee import request_attestation_from_enclave_use_case

logger = api_logger.get()


async def execute(name: str) -> TeeAttestationResponse:
    try:
        result = await request_attestation_from_enclave_use_case.execute(name)
        return TeeAttestationResponse(attestation=result)
    except Exception as e:
        logger.error(f"Error attesting enclave: {str(e)}")
        raise HTTPException(
            status_code=500, detail=f"Error attesting enclave: {str(e)}"
        )
