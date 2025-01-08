from datetime import datetime
import json
from fastapi import HTTPException
import subprocess
from service.tee.entities import TeeDeploymentResponse
from repository.enclave_repository import EnclaveRepository, EnclaveState

TEE_CPU_COUNT = 2
TEE_MEMORY_IN_MB = 8192


async def execute(
    name: str,
    version: str,
    docker_hub_image: str,
    enclave_repository: EnclaveRepository,
) -> TeeDeploymentResponse:
    enclave_eif_name = generate_eif_name(name, version)
    build_result = build_enclave(enclave_eif_name, docker_hub_image)
    print(f"Enclave built: {build_result}")

    running_result = run_enclave(enclave_eif_name)
    print(f"Enclave running: {running_result}")

    enclave_cid = json.loads(running_result).get("EnclaveCID")
    if enclave_cid is None:
        raise HTTPException(status_code=503, detail="Enclave CID not found")

    enclave_repository.add_enclave(enclave_cid, enclave_eif_name, EnclaveState.RUNNING)

    return TeeDeploymentResponse(result=running_result)


def run_command(command: list) -> str:
    try:
        result = subprocess.run(
            command,
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            text=True,
            check=True,
        )
        return result.stdout.strip()
    except subprocess.CalledProcessError as e:
        raise HTTPException(status_code=503, detail=f"Error running command: {str(e)}")


def build_enclave(enclave_eif_name: str, docker_hub_image: str) -> str:
    command = [
        "nitro-cli",
        "build-enclave",
        "--docker-uri",
        docker_hub_image,
        "--output-file",
        enclave_eif_name,
    ]
    return run_command(command)


def run_enclave(enclave_eif_name: str) -> str:
    command = [
        "nitro-cli",
        "run-enclave",
        "--cpu-count",
        f"{TEE_CPU_COUNT}",
        "--memory",
        f"{TEE_MEMORY_IN_MB}",
        "--eif-path",
        enclave_eif_name,
    ]
    return run_command(command)


def generate_eif_name(name: str, version: str) -> str:
    return f"{name}-{version}-{datetime.utcnow().strftime('%Y%m%d%H%M%S')}.eif"
