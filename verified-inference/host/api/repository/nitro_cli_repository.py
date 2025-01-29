import json
import subprocess
from typing import Dict, List, Optional
import re
import time


TEE_CPU_COUNT = 2
TEE_MEMORY_IN_MB_LOW = 4096
TEE_MEMORY_IN_MB_HIGH = 8192


class NitroCLIError(Exception):
    def __init__(self, message: str, code: Optional[str] = None):
        self.message = message
        self.code = code
        super().__init__(self.message)

    def __str__(self):
        return f"NitroCLIError(code={self.code}, message='{self.message}')"


class MemoryLimitError(NitroCLIError):
    def __init__(self, requested_memory: int, max_memory: int):
        message = (
            f"Requested memory {requested_memory} MB exceeds the maximum allowed "
            f"memory {max_memory} MB."
        )
        super().__init__(message=message)


def _run_command(command: list) -> str:
    try:
        result = subprocess.run(
            command,
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            text=True,
            check=True,
        )
        if result.stderr:
            print(f"Error logs: {result.stderr.strip()}")
        return result.stdout.strip()
    except subprocess.CalledProcessError as e:
        error_message = e.stderr.strip()
        error_code = _parse_error_code(error_message)
        raise NitroCLIError(message=error_message, code=error_code) from e


def _parse_error_code(error_message: str) -> Optional[str]:
    match = re.search(r"\[ E(\d+) \]", error_message)
    if match:
        return f"E{match.group(1)}"
    return None


def _parse_min_memory(error_message: str) -> Optional[int]:
    match = re.search(r"the minimum memory should be (\d+) MB", error_message)
    if match:
        return int(match.group(1))
    return None


def _create_run_enclave_command(enclave_name: str, memory_mb: int) -> List[str]:
    return [
        "nitro-cli",
        "run-enclave",
        "--cpu-count",
        f"{TEE_CPU_COUNT}",
        "--memory",
        f"{memory_mb}",
        "--debug-mode",
        "--eif-path",
        f"{enclave_name}.eif",
    ]


def _handle_insufficient_memory_error(enclave_name: str, error: NitroCLIError) -> Dict:
    min_memory = _parse_min_memory(error.message)
    if min_memory:
        print(f"Retrying with minimum memory: {min_memory} MB")
        time.sleep(1)  # add a small delay to avoid immediate retry
        return run_enclave(enclave_name, memory_mb=min_memory + 1024, retry=False)
    raise error


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


def run_enclave(
    enclave_name: str, memory_mb: Optional[int] = None, retry: bool = True
) -> Dict:
    memory_to_use = memory_mb if memory_mb else TEE_MEMORY_IN_MB_LOW
    if memory_to_use > TEE_MEMORY_IN_MB_HIGH:
        raise MemoryLimitError(memory_to_use, TEE_MEMORY_IN_MB_HIGH)
    command = _create_run_enclave_command(enclave_name, memory_to_use)
    try:
        res = _run_command(command)
        return json.loads(res)
    except NitroCLIError as e:
        if e.code == "E26" and retry:
            return _handle_insufficient_memory_error(enclave_name, e)
        raise


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


if __name__ == "__main__":
    try:
        print(run_enclave("067988c3-6ede-7553-8000-e7d0807256bb", memory_mb=10000))
    except NitroCLIError as e:
        print(f"Caught an error: {e}")
