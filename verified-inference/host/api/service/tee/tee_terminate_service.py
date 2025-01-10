import json
from fastapi import HTTPException
from service.tee.entities import TeeTerminateResponse
from domain.tee import terminate_enclave_use_case


async def execute(
    name: str,
) -> TeeTerminateResponse:
    try:
        result = await terminate_enclave_use_case.execute(name)

        return TeeTerminateResponse(result=result)
    except Exception as e:
        raise HTTPException(
            status_code=500, detail=f"Error terminating enclave: {str(e)}"
        )
