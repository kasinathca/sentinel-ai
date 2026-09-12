class AIIntegrationError(Exception):
    code = "AI_INTEGRATION_ERROR"


class WorkerContractValidationError(AIIntegrationError):
    code = "WORKER_RESULT_INVALID"


class UnknownModelError(AIIntegrationError):
    code = "MODEL_VERSION_UNKNOWN"


class ModelContractMismatchError(AIIntegrationError):
    code = "MODEL_CONTRACT_MISMATCH"


class OutOfOrderWorkerObservation(AIIntegrationError):
    code = "WORKER_RESULT_OUT_OF_ORDER"


class WorkerReportedFailure(AIIntegrationError):
    code = "AI_WORKER_FAILED"

    def __init__(self, worker_code: str, message: str) -> None:
        super().__init__(message)
        self.worker_code = worker_code
        self.safe_message = message
