class PackageRuntimeException(Exception):
    """ raised when agent runner is at maximum load"""
    pass


class MaxAttempts(Exception):
    """ raised when execution reached max attempts"""
    pass


class AgentRunnerFull(Exception):
    """ raised when agent runner is at maximum load"""
    pass


class UnknownResponseFromAgentRunner(Exception):
    """ raised when unknown status code received from runner"""
    pass


class RunnerNotAvailable(Exception):
    """ raised when connection failed to agent runner"""
    pass


class ParsingInputsError(Exception):
    """ raised when failed to parse executions inputs"""
    pass


class StopContainer(Exception):
    """ raised when failed to parse executions inputs"""
    pass


class RunnerReset(Exception):
    """ raised when failed to parse executions inputs"""
    pass


class MissingModule(Exception):
    """ raised when failed to parse executions inputs"""
    pass


class MissingFunction(Exception):
    """ raised when failed to parse executions inputs"""
    pass


class ExecutionProgressUpdateError(Exception):
    """ raised when failed to parse executions inputs"""
    pass


class ReportSerializationError(Exception):
    """ raised when failed to serialize report"""
    pass


class UnknownAgentMode(Exception):
    """ raised when failed to parse executions inputs"""
    pass


class UnknownOperation(Exception):
    """ raised when failed to parse executions inputs"""
    pass


class UnknownResource(Exception):
    """ raised when unknown resource is received"""
    pass

