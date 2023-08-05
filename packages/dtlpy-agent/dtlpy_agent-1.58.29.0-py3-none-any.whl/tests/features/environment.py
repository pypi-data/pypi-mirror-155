import os
from threading import Thread

from behave import fixture
# f5Gdf7!$tym45x
from dtlpy_agent.cli.parser import PackageOperations
from dtlpy_agent.proxy import RunnerHeartbeat, Bootstraper
from dtlpy_agent.services import ClientApi, AgentMode, init_prometheus_metrics
from tests.context import AgentContext
from tests.features.steps.utils.utils import create_service, start_agent, get_init_args
import dtlpy as dl

try:
    # for local import
    from tests.env_from_git_branch import get_env_from_git_branch
except ImportError:
    # for remote import
    from tests.env_from_git_branch import get_env_from_git_branch


def before_all(context: AgentContext):
    env = get_env_from_git_branch()
    dl.setenv(env=env)
    context.env = env
    dl.login_secret(email=os.environ["{}_USER_EMAIL".format(env.upper())],
                    password=os.environ["{}_USER_PASSWORD".format(env.upper())],
                    client_id=os.environ["{}_CLIENT_ID".format(env.upper())],
                    client_secret=os.environ["{}_CLIENT_SECRET".format(env.upper())])


@fixture
def before_feature(context: AgentContext, feature):
    pass


@fixture
def after_tag(context: AgentContext, tag):
    if tag == 'feature.cleanup.project':
        context.feature.project.delete(True, True)
    if tag == 'feature.cleanup.proxy':
        context.feature.proxy_process.kill()
    if tag == 'feature.cleanup.runner':
        context.feature.runner_process.kill()


@fixture
def before_tag(context: AgentContext, tag):
    if tag == 'feature.require.service':
        create_service(context=context)
    if tag == 'feature.require.proxy':
        context.feature.proxy_process = start_agent(service=context.feature.service,
                                                    env=context.env,
                                                    operation=PackageOperations.PROXY)
    if tag == 'feature.require.runner':
        context.feature.runner_process = start_agent(service=context.feature.service,
                                                     env=context.env,
                                                     operation=PackageOperations.RUNNER)
    if tag == 'scenario.require.runner_api_client':
        context.runner_api_client = ClientApi(
            mode=AgentMode.RUNNER,
            env=context.env
        )
        context.runner_api_client.setup()

    if tag == 'feature.require.proxy_bootstraper':
        args = get_init_args(service=context.feature.service,
                             env=context.env,
                             operation=PackageOperations.PROXY)
        context.bootstraper = Bootstraper(
            username=args.username,
            password=args.password,
            client_id=args.client_id,
            client_secret=args.client_secret,
            env=args.env,
            mq_host=args.mq_host,
            mq_user=args.mq_user,
            mq_password=args.mq_password,
            mq_queue=args.mq_queue,
            mq_prefetch=args.mq_prefetch,
            project_id=args.project_id,
            service_id=args.service_id,
        )
    if tag == 'feature.require.proxy_api_client':

        context.proxy_api_client = ClientApi(mode=AgentMode.PROXY,
                                     bootstraper=context.bootstraper,
                                     env=context.env)
        context.proxy_api_client.set_io_handler_service_id(context.bootstraper.service_id)

        context.proxy_api_client.setup()
    if tag == 'feature.require.proxy_without_runner':
        context.proxy_api_client = ClientApi(mode=AgentMode.PROXY,
                                             bootstraper=context.bootstraper,
                                             env=context.env)
        context.proxy_api_client.set_io_handler_service_id(context.bootstraper.service_id)

        context.proxy_api_client._bootstraper.setup()
        context.proxy_api_client._start_monitoring()
        context.proxy_api_client._start_execution_monitor()
        context.proxy_api_client._start_time_series_monitoring()
        context.proxy_api_client.prometheus_metrics = init_prometheus_metrics()
        context.proxy_api_client._start_piper_reporting_service()
        context.proxy_api_client.start_local_server()
        # self._io_handler.set_runner_id(self.wait_for_runner())
        context.proxy_api_client._start_runner_heartbeat()
        context.t = Thread(target=context.proxy_api_client.wait_for_runner())
        context.t.start()
    if tag == 'feature.require.runner_heartbeat':
        context.runner_heartbeat = RunnerHeartbeat(context.proxy_api_client)

    if tag.startswith('globals.'):
        attr = tag.replace('globals.', '')
        setattr(context, attr, getattr(context.feature, attr))
