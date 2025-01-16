import re

from fastapi import APIRouter
from fastapi import Depends
from fastapi import HTTPException
from fastapi import Request

from service.tee.entities import (
    TeeAttestationResponse,
    TeeDeploymentRequest,
    TeeDeploymentResponse,
    TeeTerminateRequest,
    TeeTerminateResponse,
    TeeGetEnclaveResponse,
)
from service.tee import (
    tee_deploy_service,
    tee_attestation_service,
    tee_terminate_service,
    tee_get_enclave_service,
)

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
):
    return await tee_deploy_service.execute(
        request.enclave_name,
        request.docker_hub_image,
        request.env_vars,
    )


@router.post(
    "/terminate",
    summary="Terminate the enclave.",
    description="Terminate the enclave with the given name.",
    response_description="Returns the termination result",
    response_model=TeeTerminateResponse,
)
async def terminate(
    api_request: Request,
    request: TeeTerminateRequest,
):
    return await tee_terminate_service.execute(request.enclave_name)


@router.get(
    "/enclave/{enclave_name}",
    summary="Get the enclave information.",
    description="Get the enclave information of the given enclave name.",
    response_description="Returns the enclave information",
    response_model=TeeGetEnclaveResponse,
)
async def enclave(
    api_request: Request,
    enclave_name: str,
):
    return await tee_get_enclave_service.execute(enclave_name)


@router.get(
    "/attestation/{enclave_name}",
    summary="Get the attestation document for the enclave.",
    description="Get the attestation document for the enclave.",
    response_description="Returns the attestation document",
    response_model=TeeAttestationResponse,
)
async def attestation(
    api_request: Request,
    enclave_name: str,
):
    return await tee_attestation_service.execute(enclave_name)
