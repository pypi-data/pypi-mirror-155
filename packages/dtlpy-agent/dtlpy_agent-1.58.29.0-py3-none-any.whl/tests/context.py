from behave.runner import Context
import dtlpy as dl

from dtlpy_agent.proxy import RunnerHeartbeat, Bootstraper
from dtlpy_agent.runner import Runner, RunnerMonitoring
from dtlpy_agent.services import ClientApi


class AgentContext(Context):
    def __init__(self, runner):
        super(AgentContext, self).__init__(runner=runner)
        self.project: dl.entities.Project = None
        self.service: dl.entities.Service = None
        self.runner_api_client: ClientApi = None
        self.proxy_api_client: ClientApi = None
        self.runner_heartbeat: RunnerHeartbeat = None
        self.bootstraper: Bootstraper = None
        self.proxy_monitoring: RunnerMonitoring = None
        self.runner: Runner = None
