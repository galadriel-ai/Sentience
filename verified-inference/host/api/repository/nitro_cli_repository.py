import json
import subprocess
from typing import Dict, List


TEE_CPU_COUNT = 2
TEE_MEMORY_IN_MB = 8192


def _run_command(command: list) -> str:
    try:
        result = subprocess.run(
            command,
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            text=True,
            check=True,
        )
        # Return the combined stdout and stderr for logging purposes
        return result.stdout + result.stderr
    except subprocess.CalledProcessError as e:
        print(f"Error running command: {str(e)}")
        raise e


def build_enclave(enclave_name: str, docker_hub_image: str) -> Dict:
    command = [
        "nitro-cli",
        "build-enclave",
        "--docker-uri",
        docker_hub_image,
        "--output-file",
        f"{enclave_name}.eif",
    ]
    res = _run_command(command)
    return json.loads(res)


def run_enclave(enclave_name: str) -> Dict:
    command = [
        "nitro-cli",
        "run-enclave",
        "--cpu-count",
        f"{TEE_CPU_COUNT}",
        "--memory",
        f"{TEE_MEMORY_IN_MB}",
        "--eif-path",
        f"{enclave_name}.eif",
    ]
    res = _run_command(command)
    return json.loads(res)


def terminate_enclave(enclave_name: str) -> Dict:
    command = [
        "nitro-cli",
        "terminate-enclave",
        "--enclave-name",
        enclave_name,
    ]
    res = _run_command(command)
    return json.loads(res)


def describe_enclaves() -> List[Dict]:
    command = [
        "nitro-cli",
        "describe-enclaves",
    ]
    res = _run_command(command)
    return json.loads(res)
