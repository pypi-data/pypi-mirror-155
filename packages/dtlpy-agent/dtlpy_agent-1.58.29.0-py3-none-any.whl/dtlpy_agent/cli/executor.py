import os
import sys
from contextlib import redirect_stdout, redirect_stderr
from ..proxy import Bootstraper, Proxy
from ..runner import Runner
from ..services import ClientApi, AgentMode, AgentStreamHandler, AgentRedirect
from .. import exceptions
from .parser import PackageOperations
import logging


def redirect(api_client):
    #####################
    # MUST BE like that #
    #####################
    # create handle to stdout with the redirect
    handler = AgentStreamHandler(api_client=api_client)
    handler.setLevel(logging.DEBUG)
    handler.setFormatter(logging.Formatter('%(name)s - %(levelname)s - %(thread)d - %(message)s'))
    root = logging.getLogger()

    # remove all other handlers
    root.handlers = list()

    root.addHandler(handler)
    redirected_stdout = AgentRedirect(logger=root, std_type=AgentRedirect.STDOUT)
    redirected_stderr = AgentRedirect(logger=root, std_type=AgentRedirect.STDERR)
    logging.getLogger('urllib3').setLevel(logging.WARN)
    logging.getLogger('tornado').setLevel(logging.WARN)
    logging.getLogger('filelock').setLevel(logging.WARN)
    return redirected_stdout, redirected_stderr


def run_agent(args):
    with_redirect = os.environ.get('WITH_REDIRECT', 'true') == 'true'
    redirected_stdout = None
    redirected_stderr = None

    if args.operation == PackageOperations.RUNNER:

        api_client = ClientApi(
            mode=AgentMode.RUNNER,
            env=args.env
        )
        api_client.set_io_handler_project_id(args.project_id)

        if with_redirect:
            redirected_stdout, redirected_stderr = redirect(api_client=api_client)
            
        api_client.setup()
        runner = Runner(api_client=api_client)

        if with_redirect:
            with redirect_stdout(redirected_stdout), redirect_stderr(redirected_stderr):
                runner.start(project_id=args.project_id, service_id=args.service_id)
        else:
            runner.start(project_id=args.project_id, service_id=args.service_id)
        sys.exit(0)

    elif args.operation in [PackageOperations.PROXY, PackageOperations.SINGLE]:
        bootstraper = Bootstraper(
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

        if args.operation == PackageOperations.PROXY:
            api_client = ClientApi(
                mode=AgentMode.PROXY,
                bootstraper=bootstraper,
                env=args.env
            )
        else:
            api_client = ClientApi(
                bootstraper=bootstraper,
                mode=AgentMode.SINGLE_AGENT,
                env=args.env
            )

        api_client.set_io_handler_service_id(args.service_id)
        api_client.set_io_handler_project_id(args.project_id)

        def start():
            api_client.setup()
            if args.operation == PackageOperations.SINGLE:
                # noinspection PyShadowingNames
                runner = Runner(api_client=api_client)
                runner.start(project_id=args.project_id, service_id=args.service_id)

            proxy = Proxy(api_client=api_client)
            proxy.start()

        if with_redirect:
            redirected_stdout, redirected_stderr = redirect(api_client=api_client)
            with redirect_stdout(redirected_stdout), redirect_stderr(redirected_stderr):
                start()
        else:
            start()

        sys.exit(0)
    else:
        raise exceptions.UnknownOperation('Unknown dtlpy-agent operation: {}'.format(args.operation))
