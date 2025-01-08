from pydantic import BaseModel
from pydantic import Field


class TeeDeploymentRequest(BaseModel):
    enclave_name: str = Field(description="Enclave name")
    enclave_version: str = Field(description="Enclave version")
    docker_hub_image: str = Field(
        description="Docker Hub image name in the format <repository>:<tag>"
    )


class TeeDeploymentResponse(BaseModel):
    result: str = Field(description="Deployment result")
