from typing import Dict
from pydantic import BaseModel
from pydantic import Field


class TeeDeploymentRequest(BaseModel):
    enclave_name: str = Field(description="Enclave name")
    docker_hub_image: str = Field(
        description="Docker Hub image name in the format <repository>:<tag>"
    )


class TeeDeploymentResponse(BaseModel):
    result: Dict = Field(description="Deployment result")


class TeeTerminateRequest(BaseModel):
    enclave_name: str = Field(description="Enclave name")


class TeeTerminateResponse(BaseModel):
    result: Dict = Field(description="Termination result")


class TeeGetEnclaveResponse(BaseModel):
    enclave_name: str = Field(description="Enclave name")
    enclave_cid: int = Field(description="Enclave CID")
    enclave_status: str = Field(description="Enclave status")


class TeeAttestationResponse(BaseModel):
    attestation: str = Field(description="Attestation document")
