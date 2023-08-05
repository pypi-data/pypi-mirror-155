import os
from .features.steps.runner import runner_load_package
from .features.steps.services import api_client_runner, api_client_proxy
from .features.steps.services import waiting_for_proxy, wating_for_runner
from .features.steps.proxy import runner_heartbeat_proxy
from .features.steps.proxy import bootstraper_proxy
from .features.steps.proxy import proxt_local_service
from .features.steps.runner import runner_usade

os.environ['AGENT_TEST_ASSETS'] = os.path.join(os.getcwd(), 'tests', 'assets')
