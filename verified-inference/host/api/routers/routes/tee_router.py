import re

from fastapi import APIRouter
from fastapi import Depends
from fastapi import Header
from fastapi import HTTPException
from fastapi import Request

import dependencies
from service.tee.entities import TeeDeploymentRequest, TeeDeploymentResponse
from service.tee import tee_deploy_service

TAG = "TEE"
router = APIRouter(prefix="/tee")
router.tags = [TAG]


@router.post(
    "/deploy",
    summary="Build and deploy the provided docker image to the TEE.",
    description="Given a docker image from docker hub, the model will build and deploy it to the TEE.",
    response_description="Returns the deployment result",
    response_model=TeeDeploymentResponse,
)
async def deploy(
    api_request: Request,
    request: TeeDeploymentRequest,
    enclave_repository=Depends(dependencies.get_enclave_repository),
):
    return await tee_deploy_service.execute(
        request.enclave_name, request.enclave_version, request.docker_hub_image, enclave_repository
    )
