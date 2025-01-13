import subprocess


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
        return result.stdout.strip()
    except subprocess.CalledProcessError as e:
        print(f"Error running command: {str(e)}")
        raise e


def build_enclave(enclave_name: str, docker_hub_image: str) -> str:
    command = [
        "nitro-cli",
        "build-enclave",
        "--docker-uri",
        docker_hub_image,
        "--output-file",
        f"{enclave_name}.eif",
    ]
    return _run_command(command)


def run_enclave(enclave_name: str) -> str:
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
    return _run_command(command)


def terminate_enclave(enclave_name: str) -> str:
    command = [
        "nitro-cli",
        "terminate-enclave",
        "--enclave-name",
        enclave_name,
    ]
    return _run_command(command)


def describe_enclaves() -> str:
    command = [
        "nitro-cli",
        "describe-enclaves",
    ]
    return _run_command(command)
