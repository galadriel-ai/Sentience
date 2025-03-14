from typing import List
from fastapi import HTTPException

import api_logger

from service.tee.entities import TeeGetEnclaveResponse, TeeGetEnclavesResponse
from domain.tee import get_all_enclaves_use_case

logger = api_logger.get()


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
        logger.error(f"Error getting all enclaves: {str(e)}")
        raise HTTPException(status_code=500, detail=f"Error: {str(e)}")
