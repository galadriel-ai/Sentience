import asyncio
from enum import Enum
import json
import subprocess
from typing import Dict, Optional
from utils import proxy_manager


class EnclaveState(Enum):
    RUNNING = "running"
    STOPPED = "stopped"


class Enclave:
    proxy_task: Optional[asyncio.Task] = None

    def __init__(self, enclave_name: str, state: EnclaveState):
        self.enclave_name = enclave_name
        self.state = state


class EnclaveRepository:
    _enclaves: Dict[str, Enclave] = {}

    def __init__(self):
        with subprocess.Popen(
            ["/bin/nitro-cli", "describe-enclaves"], stdout=subprocess.PIPE
        ) as proc:
            output = json.loads(proc.communicate()[0].decode())
            for enclave in output:
                self._enclaves[enclave["EnclaveCID"]] = Enclave(
                    enclave["EnclaveName"], EnclaveState(enclave["State"].lower())
                )

    def get_enclave(self, enclave_cid: str) -> Optional[Enclave]:
        return self._enclaves.get(enclave_cid)

    def get_all_enclaves(self) -> Dict[str, Enclave]:
        return self._enclaves

    def add_enclave(self, enclave_cid: str, enclave_name: str, state: EnclaveState):
        self._enclaves[enclave_cid] = Enclave(enclave_cid, state)
        self._start_enclave_proxy(enclave_cid)
        print(f"Enclave {enclave_cid} added to repository")

    def remove_enclave(self, enclave_cid: str):
        if enclave_cid in self._enclaves:
            self._stop_enclave_proxy(self._enclaves[enclave_cid])
            del self._enclaves[enclave_cid]
            print(f"Enclave {enclave_cid} removed from repository")
        else:
            raise ValueError(f"Enclave {enclave_cid} not found in repository")

    def _start_enclave_proxy(self, enclave_cid: str):
        self._enclaves[enclave_cid].proxy_task = asyncio.create_task(
            proxy_manager.run_proxy_service(enclave_cid)
        )

    def _stop_enclave_proxy(self, enclave: Enclave):
        if enclave.proxy_task:
            enclave.proxy_task.cancel()
            enclave.proxy_task = None
