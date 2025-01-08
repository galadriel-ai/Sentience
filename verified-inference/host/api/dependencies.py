from repository.enclave_repository import EnclaveRepository

enclave_repository: EnclaveRepository


# pylint: disable=W0603
def init_globals():
    global enclave_repository

    enclave_repository = EnclaveRepository()


def get_enclave_repository() -> EnclaveRepository:
    return enclave_repository
