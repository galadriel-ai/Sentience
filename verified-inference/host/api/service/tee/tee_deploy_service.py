from fastapi import HTTPException
from service.tee.entities import TeeDeploymentResponse
from domain.tee import deploy_enclave_use_case


async def execute(
    name: str,
    docker_hub_image: str,
) -> TeeDeploymentResponse:
    try:
        result = await deploy_enclave_use_case.execute(name, docker_hub_image)
        return TeeDeploymentResponse(result=result)
    except Exception as e:
        raise HTTPException(
            status_code=500, detail=f"Error deploying enclave: {str(e)}"
        )
