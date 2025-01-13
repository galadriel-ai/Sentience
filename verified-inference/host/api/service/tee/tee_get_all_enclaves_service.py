from typing import List
from fastapi import HTTPException
from service.tee.entities import TeeGetEnclaveResponse, TeeGetEnclavesResponse
from domain.tee import get_all_enclaves_use_case


async def execute() -> TeeGetEnclavesResponse:
    try:
        enclaves = await get_all_enclaves_use_case.execute()
        return TeeGetEnclavesResponse(
            enclaves=[
                TeeGetEnclaveResponse(
                    enclave_name=enclave.name,
                    enclave_cid=enclave.cid,
                    enclave_status=enclave.state.value,
                )
                for enclave in enclaves.values()
            ]
        )
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error: {str(e)}")
