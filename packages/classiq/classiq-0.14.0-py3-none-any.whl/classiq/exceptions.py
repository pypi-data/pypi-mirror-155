import logging

_logger = logging.getLogger(__name__)


class ClassiqError(Exception):
    def __init__(self, message: str) -> None:
        super().__init__(message)
        _logger.error("%s\n", message)


class ClassiqExecutionError(ClassiqError):
    pass


class ClassiqDefaultQuantumProgramError(ClassiqError):
    def __init__(self) -> None:
        message = "Default program unavailable, please generate a QuantumProgram object manually"
        super().__init__(message=message)


class ClassiqGenerationError(ClassiqError):
    pass


class ClassiqCombinatorialOptimizationError(ClassiqError):
    pass


class ClassiqAnalyzerError(ClassiqError):
    pass


class ClassiqAnalyzerGraphError(ClassiqError):
    pass


class ClassiqAPIError(ClassiqError):
    pass


class ClassiqVersionError(ClassiqError):
    pass


class ClassiqValueError(ClassiqError, ValueError):
    pass


class ClassiqWiringError(ClassiqValueError):
    pass


class ClassiqQRegError(ClassiqValueError):
    pass


class ClassiqQFuncError(ClassiqValueError):
    pass


class ClassiqQSVMError(ClassiqValueError):
    pass


class ClassiqAuthenticationError(ClassiqError):
    pass


class ClassiqExpiredTokenError(ClassiqAuthenticationError):
    pass


class ClassiqFileNotFoundError(FileNotFoundError):
    pass
