from typing import Any
from typing import Dict
from fastapi import HTTPException
from service.tee.entities import TeeDeploymentResponse
from domain.tee import deploy_enclave_use_case
from domain.tee import inject_env_vars_use_case


async def execute(
    name: str, docker_hub_image: str, env_vars: Dict[str, Any]
) -> TeeDeploymentResponse:
    try:
        result = await deploy_enclave_use_case.execute(name, docker_hub_image, env_vars)
        await inject_env_vars_use_case.execute(result["EnclaveCID"], env_vars)
        return TeeDeploymentResponse(result=result)
    except Exception as e:
        raise HTTPException(
            status_code=500, detail=f"Error deploying enclave: {str(e)}"
        )
