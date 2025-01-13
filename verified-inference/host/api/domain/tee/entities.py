from dataclasses import dataclass
from enum import Enum


class EnclaveState(Enum):
    RUNNING = "RUNNING"
    TERMINATING = "TERMINATING"


@dataclass
class Enclave:
    name: str
    cid: int
    state: EnclaveState
