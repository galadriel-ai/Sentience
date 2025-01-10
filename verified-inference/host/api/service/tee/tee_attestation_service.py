from fastapi import HTTPException
from service.tee.entities import TeeAttestationResponse
from domain.tee import request_attestation_from_enclave_use_case


async def execute(name: str) -> TeeAttestationResponse:
    try:
        result = await request_attestation_from_enclave_use_case.execute(name)
        return TeeAttestationResponse(result=result)
    except Exception as e:
        raise HTTPException(
            status_code=500, detail=f"Error attesting enclave: {str(e)}"
        )
