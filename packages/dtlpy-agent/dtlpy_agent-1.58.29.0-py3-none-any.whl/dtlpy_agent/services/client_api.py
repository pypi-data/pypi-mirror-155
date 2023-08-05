import json
import dateutil.parser
from multiprocessing import Queue, Process
import dateutil.parser
from tornado.httpserver import HTTPServer
from tornado.netutil import bind_sockets
from dtlpy.new_instance import Dtlpy
from threading import Thread
from tornado import concurrent
from inspect import signature
from typing import Union
import tornado.ioloop
import tornado.escape
import dtlpy as dl
import tornado.web
import tornado
import asyncio
import threading
import traceback
import tempfile
import requests
import logging
import psutil
import socket
import signal
import uuid
import time
import os
from . import IOHandler, init_prometheus_metrics, RequestSession, WebSocketClient
from ..proxy.ampq_connection_publisher import ServiceStatusReport, ExecutionStatusReport, RabbitMqPublisherClient
from ..runner import RunnerMonitoring, WebServer, Progress, ExternalHttpServer
from ..proxy import MainWebServer, PrometheusWebServer, Monitoring, TimeSeriesMonitoring, RunnerHeartbeat, \
    ExecutionMonitor
from dtlpy_agent import exceptions
from .termination_handlers import TerminationHandler

logger = logging.getLogger('AgentRunner.ApiClient')


class AgentMode:
    PROXY = 'proxy'
    RUNNER = 'runner'
    SINGLE_AGENT = 'single'


class ClientApi:
    def __init__(
            self,
            mode: str,
            bootstraper=None,
            env: str = None,
            mq=None
    ):

        self.proxy_port = os.environ.get('AGENT_PROXY_MAIN_PORT') or "1001"
        self.prometheus_port = os.environ.get('AGENT_PROXY_PROMETHEUS_PORT') or "9521"
        self.runner_port = os.environ.get('AGENT_RUNNER_MAIN_PORT') or "8889"
        self.external_port = os.environ.get('EXTERNAL_MAIN_PORT') or "3000"
        # self.main_address = None
        self.main_address = '127.0.0.1' if env != 'local' else None
        self.mode = mode
        self._io_handler = IOHandler()
        self.termination_handler = TerminationHandler(client_api=self)
        self.requests_session = RequestSession()
        self.functions_params_check = dict()

        # proxy attributes
        self.prometheus_metrics = None
        self._monitoring = None
        self._bootstraper = bootstraper
        self.pod_socket_name = socket.gethostname()
        self._system_and_uptime_monitoring = None
        self._execution_monitoring = None
        self._mq = mq
        self.proxy_ws_client = WebSocketClient(url="ws://localhost:{}/web-socket".format(self.runner_port))

        # runner attributes
        self._project = None
        self._package = None
        self._service = None
        self._env = env
        self._runner_monitoring = None
        self.service_runner = None
        self._executor = None
        self.package_path = None
        self.runner_report_ws_client = WebSocketClient(
            url="ws://localhost:{}/execution_report".format(self.proxy_port)
        )
        self.runner_status_ws_client = WebSocketClient(
            url="ws://localhost:{}/execution_status_update".format(self.proxy_port)
        )

    ##############
    # properties #
    ##############

    @property
    def package(self) -> dl.entities.Package:
        if self.mode in [AgentMode.SINGLE_AGENT, AgentMode.PROXY]:
            return self._bootstraper.package
        else:
            return self._package

    @package.setter
    def package(self, package: dl.entities.Package):
        if self.mode in [AgentMode.PROXY]:
            raise Exception('Cannot set api_client.project in proxy')
        else:
            self._package = package

    @property
    def service(self) -> dl.entities.Service:
        if self.mode in [AgentMode.SINGLE_AGENT, AgentMode.PROXY]:
            return self._bootstraper.service
        else:
            return self._service

    @service.setter
    def service(self, service: dl.entities.Service):
        if self.mode in [AgentMode.PROXY]:
            raise Exception('Cannot set api_client.service in proxy')
        else:
            self._service = service

    @property
    def project(self) -> dl.entities.Project:
        if self.mode in [AgentMode.SINGLE_AGENT, AgentMode.PROXY]:
            return self._bootstraper.project
        else:
            return self._project

    @project.setter
    def project(self, project: dl.entities.Project):
        if self.mode in [AgentMode.PROXY]:
            raise Exception('Cannot set api_client.project in proxy')
        else:
            self._project = project

    @property
    def env(self) -> str:
        if self.mode in [AgentMode.SINGLE_AGENT, AgentMode.PROXY]:
            return self._bootstraper.env
        else:
            return self._env

    @property
    def monitoring(self) -> Monitoring:
        return self._monitoring

    @property
    def runner_monitoring(self) -> RunnerMonitoring:
        return self._runner_monitoring

    @property
    def system_and_uptime_monitoring(self) -> TimeSeriesMonitoring:
        return self._system_and_uptime_monitoring

    @property
    def run_execution_as_process(self) -> bool:
        return self.service.run_execution_as_process

    @property
    def user_log_phrase(self) -> str:
        return self._io_handler.user_log_phrase

    @property
    def num_workers(self) -> int:
        return self._io_handler.num_workers

    @property
    def entities_json(self) -> dict:
        _json = dict()
        if self.project:
            _json['project'] = self.project.to_json()
        if self.service:
            _json['service'] = self.service.to_json()
        if self.package:
            _json['package'] = self.package.to_json()

        return _json

    @property
    def use_user_jwt(self):
        return hasattr(self.service, 'use_user_jwt') and self.service.use_user_jwt

    @property
    def executions_in_progress(self):
        return self._io_handler.executions_in_progress

    @property
    def executor(self):
        if self._executor is None:
            self._executor = concurrent.futures.ThreadPoolExecutor(self.num_workers)
        return self._executor

    @property
    def run_as_process(self):
        return hasattr(self.service, 'run_execution_as_process') and self.service.run_execution_as_process

    @property
    def execution_end_line(self):
        return dl.FUNCTION_END_LINE if hasattr(dl, 'FUNCTION_END_LINE') else "[Done] Executing function."

    ################
    # Initializing #
    ################

    def setup(self):
        self._set_sigterm_method()

        # proxy and local setup
        if self.mode in [AgentMode.PROXY, AgentMode.SINGLE_AGENT]:
            self._bootstraper.setup()
            self._start_monitoring()
            self._start_execution_monitor()
            self._start_time_series_monitoring()
            self.prometheus_metrics = init_prometheus_metrics()
            self._start_piper_reporting_service()

        # runner and local setup
        if self.mode in [AgentMode.RUNNER, AgentMode.SINGLE_AGENT]:
            self._io_handler.set_runner_id(str(uuid.uuid1()))
            dl.setenv(self.env)

        # proxy-only setup
        if self.mode == AgentMode.PROXY:
            self.start_local_server()
            self._io_handler.set_runner_id(self.wait_for_runner())
            self._start_runner_heartbeat()
            self.init_proxy_ws_client()

    def init_proxy_ws_client(self):
        self.proxy_ws_client.init()

    def init_runner_ws_client(self):
        self.runner_report_ws_client.init()
        self.runner_status_ws_client.init()

    def start_runner_monitoring(self):
        logger.info('[Start] setting up RunnerMonitoring server')
        self._runner_monitoring = RunnerMonitoring(client_api=self)
        self._runner_monitoring.daemon = True
        self._runner_monitoring.start()
        self._runner_monitoring.report_up()
        logger.info('[Done] setting up RunnerMonitoring server')

    def _start_execution_monitor(self):
        logger.info('[Start] setting up ExecutionMonitor server')
        self._execution_monitoring = ExecutionMonitor(api_client=self, service=self.service)
        self._execution_monitoring.daemon = True
        self._execution_monitoring.start()
        logger.info('[Done] setting up ExecutionMonitor server')

    def _start_piper_reporting_service(self):
        logger.info('[Start] setting up RabbitMqPublisherClient server')
        self._reporting_service = RabbitMqPublisherClient(
            api_client=self,
            hostname=self._bootstraper.mq_host,
            username=self._bootstraper.mq_user,
            password=self._bootstraper.mq_password
        )
        self._reporting_service.daemon = True
        self._reporting_service.start()
        logger.info('[Done] setting up RabbitMqPublisherClient server')

    # noinspection PyUnusedLocal
    def _runner_sigterm_handler(self, signum, frame):
        logger.info("[SIGTERM RECEIVED] starting termination handler.")
        self.termination_handler.runner_termination_handler()

    # noinspection PyUnusedLocal
    def _proxy_sigterm_handler(self, signum, frame):
        logger.info("[SIGTERM RECEIVED] starting termination handler.")
        self.termination_handler.proxy_termination_handler()

    def _set_sigterm_method(self):
        if self.mode in [AgentMode.PROXY, AgentMode.SINGLE_AGENT]:
            signal.signal(signal.SIGTERM, self._proxy_sigterm_handler)
        else:
            signal.signal(signal.SIGTERM, self._runner_sigterm_handler)

    def start_runner_server(self):
        try:
            asyncio.set_event_loop(asyncio.new_event_loop())
            m_server = WebServer(client_api=self)
            # proxy will listen only on localhost
            main_sockets = bind_sockets(
                port=int(self.runner_port),
                address=self.main_address
            )
            main_server = HTTPServer(m_server)
            main_server.add_sockets(main_sockets)
            logger.info(
                "Agent Runner Main server is up and listening on port {}".format(self.runner_port))
            package_type = os.environ.get("PACKAGE_TYPE", 'regular')
            if package_type == 'app':
                p_server = ExternalHttpServer(client_api=self)
                external_sockets = bind_sockets(port=int(self.external_port))
                external_server = HTTPServer(p_server)
                external_server.add_sockets(external_sockets)
                logger.info("Agent Runner External server is up and listening on port {}".format(self.external_port))

            tornado.ioloop.IOLoop.instance().start()
        except Exception:
            logger.exception('Failed starting runner servers!')

    def start_local_server(self):
        if self.mode in [AgentMode.PROXY, AgentMode.SINGLE_AGENT]:
            logger.info('[Start] Starting proxy local server')
            t = Thread(target=self.start_proxy_server)
            t.daemon = True
            t.start()
            return t
        else:
            logger.info('[Start] Starting runner local server')
            t = Thread(target=self.start_runner_server)
            t.daemon = True
            t.start()
            return t

    def _start_monitoring(self):
        logger.info('[Start] setting up Monitoring server')
        tic_uptime = time.time()
        self._monitoring = Monitoring(
            service=self.service,
            api_client=self,
            project=self.project,
            pod_socket_name=self.pod_socket_name,
            tic_uptime=tic_uptime
        )
        self._monitoring.daemon = True
        self._monitoring.start()
        self._monitoring.set_status(value='initializing')
        logger.info('[Done] setting up Monitoring server')

    def _start_time_series_monitoring(self):
        logger.info('[Start] setting up TimeSeriesMonitoring server')
        self._system_and_uptime_monitoring = TimeSeriesMonitoring(
            service=self.service,
            pod_socket_name=self.pod_socket_name,
            project=self.project,
            api_client=self
        )
        self._system_and_uptime_monitoring.daemon = True
        self._system_and_uptime_monitoring.start()
        logger.info('[Done] setting up TimeSeriesMonitoring server')

    def _start_runner_heartbeat(self):
        logger.info('[Start] starting runner heartbeat')
        runner_heartbeat = RunnerHeartbeat(api_client=self)
        runner_heartbeat.daemon = True
        runner_heartbeat.start()
        logger.info('[Done] starting runner heartbeat')

    def wait_for_runner(self):
        logger.info('[Start] Waiting for runner')

        while True:
            try:
                if self.is_runner_available():
                    runner_id = self.get_runner_id()
                    break
                time.sleep(1)
            except Exception:
                logger.info('[InProgress] Waiting for runner')
                time.sleep(1)
        logger.info('[Done] Waiting for runner')

        return runner_id

    #####################
    # IO Handler Access #
    #####################

    def runner_started(self):
        self._io_handler.runner_started()

    def set_io_handler_service_id(self, service_id: str):
        return self._io_handler.set_service_id(service_id)

    def set_io_handler_project_id(self, project_id: str):
        return self._io_handler.set_project_id(project_id)

    def get_header(self, thread_id: int):
        return self._io_handler.get_header(thread_id=thread_id)

    def kill_process(self, execution_id: str):
        return self._io_handler.kill_process(execution_id=execution_id)

    def kill_thread(self, execution_id: str):
        return self._io_handler.kill_thread(execution_id=execution_id, service_runner=self.service_runner)

    def set_num_workers(self, num_workers: int):
        self._io_handler.num_workers = num_workers

    def redirect_thread_logs(self, thread_id: int, execution: dict, function_name: str):
        pipeline = execution.get('pipeline', None) if execution is not None else None
        self._io_handler.add_thread_to_logging(
            thread_id=thread_id,
            execution_id=execution.get('id', '') if execution is not None else '',
            function_name=function_name,
            pipeline_id=pipeline.get('id', '') if pipeline is not None else '',
            pipeline_execution_id=pipeline.get('executionId', '') if pipeline is not None else '',
            node_id=pipeline.get('nodeId', '') if pipeline is not None else '',
            project_id=execution.get('projectId', '') if execution is not None else ''
        )

    def set_restart(self, restart: bool):
        self._io_handler.set_restart(restart=restart)

    def set_runner_id(self, runner_id: str):
        self._io_handler.set_runner_id(runner_id=runner_id)

    def handle_runner_reset(self, force_all: bool = False):
        self._io_handler.handle_runner_reset(force_all=force_all)

    def executions_snapshot(self):
        return self._io_handler.executions_snapshot()

    def is_active_execution(self, execution_id):
        return self._io_handler.is_active_execution(execution_id=execution_id)

    def set_execution_by_runner(self, execution_id):
        try:
            return self._io_handler.set_execution_by_runner(execution_id=execution_id)
        except Exception:
            logger.exception('Failed to set execution by runner - restarting Service.')
            self.termination_handler.proxy_termination_handler()

    def pop_from_proxy_execution(self, execution_id: str):
        return self._io_handler.pop_from_proxy_execution(execution_id=execution_id)

    def set_execution_by_reset(self, execution_id):
        return self._io_handler.set_execution_by_reset(execution_id=execution_id)

    def undo_redirect_thread_logs(self, thread_id: int):
        self._io_handler.pop_thread_from_logging(thread_id=thread_id)

    def get_from_report_queue(self) -> Union[ServiceStatusReport, ExecutionStatusReport]:
        return self._io_handler.get_from_report_queue()

    def push_to_report_queue(self, report: Union[ServiceStatusReport, ExecutionStatusReport]):
        self._io_handler.push_to_report_queue(report=report)

    def queue_is_empty(self) -> bool:
        return self._io_handler.queue_is_empty()

    @property
    def num_inprogress_executions(self) -> int:
        return self._io_handler.num_inprogress

    @property
    def reporting_queue_empty(self):
        return self._io_handler.queue_empty

    def get_report_queue_size(self):
        return self._io_handler.get_report_queue_size()

    ##############
    # MQ Methods #
    ##############
    def stop_consuming(self):
        if self._mq is not None:
            self._mq.pause()

    def start_consuming(self, on_message):
        self._mq = self._bootstraper.get_ampq_mq_connection(
            on_message=on_message,
            on_failure=self.send_execution_update_to_proxy
        )
        self._io_handler.mq = self._mq
        logger.info('MQ Subscriber start')
        self._mq.start()

    ##############
    # Monitoring #
    ##############
    def set_monitoring_status(self, status: str):
        if self.mode in [AgentMode.RUNNER, AgentMode.SINGLE_AGENT]:
            self.runner_monitoring.set_status(value=status)
        if self.mode in [AgentMode.PROXY, AgentMode.SINGLE_AGENT]:
            self.monitoring.set_status(value=status)

    def reset_monitoring_status(self):
        if self.mode == AgentMode.PROXY:
            self.monitoring.set_status(value='down')

    def _bump_monitoring_up_counter(self):
        self.monitoring.bump_up_counter()

    def _update_usage(self, usage):
        self.system_and_uptime_monitoring.set_report(report=usage)

    def get_information_interval(self) -> int:
        if self.mode == AgentMode.RUNNER:
            resp = self.requests_session.get(
                port=self.proxy_port,
                name='information_report'
            )
            if not resp.ok:
                logger.exception("Failed to get information from proxy:")
            return resp.json()['usage_interval']
        else:
            return self._io_handler.intervals['usage_interval']

    def update_service_status(self, report: ServiceStatusReport):
        self.push_to_report_queue(report=report)

    def handle_prometheus_update(self, args: dict) -> bool:
        try:
            self._update_prometheus_metrics(args=args)
            success = True
        except Exception:
            logger.exception('Failed to update prometheus metrics')
            success = False
        return success

    def _update_prometheus_metrics(self, args: dict):
        for key, val in args.items():
            if key == 'executionStatus':
                self.prometheus_metrics['executions_total'].labels(
                    serviceName=self.service.name,
                    functionName=val['functionName'],
                    executionStatus=val['executionStatus']).inc()
            elif key == 'executionDuration':
                self.prometheus_metrics['executions_time_seconds'].labels(
                    serviceName=self.service.name,
                    functionName=val['functionName'],
                    executionStatus=val['executionStatus']).observe(
                    val['duration'])
                self.prometheus_metrics['executions_time_since_creation_seconds'].labels(
                    serviceName=self.service.name,
                    functionName=val['functionName'],
                    executionStatus=val['executionStatus']).observe(
                    val['total_duration'])
            elif key == 'memoryCpuUsage':
                self.prometheus_metrics['ram_metric'].labels(
                    serviceName=self.service.name,
                    container='proxy',
                    hostname=socket.gethostname()).set(psutil.Process().memory_info().rss)
                self.prometheus_metrics['cpu_metric'].labels(
                    serviceName=self.service.name,
                    container='proxy',
                    hostname=socket.gethostname()).set(psutil.Process().cpu_percent(3))
                self.prometheus_metrics['ram_metric'].labels(
                    serviceName=self.service.name,
                    container='runner',
                    hostname=socket.gethostname()).set(val['ram'])
                self.prometheus_metrics['cpu_metric'].labels(
                    serviceName=self.service.name,
                    container='runner',
                    hostname=socket.gethostname()).set(val['cpu'])
            else:
                logger.error('Unknown prometheus report: {}'.format(key))

    ##################
    # Global Methods #
    ##################

    def is_runner_available(self) -> bool:
        if self.mode in [AgentMode.RUNNER, AgentMode.SINGLE_AGENT]:
            return self._io_handler.is_available()
        else:
            response = self.requests_session.get(
                port=self.runner_port,
                timeout=10
            )
            return response.status_code == 200

    def is_runner_full(self) -> bool:
        if self.mode in [AgentMode.RUNNER, AgentMode.SINGLE_AGENT]:
            return self._io_handler.is_full
        else:
            raise Exception('is_runner_full method is not available in proxy mode')

    @property
    def local_runner_id(self):
        return self._io_handler.get_runner_id()

    def get_runner_id(self):
        if self.mode in [AgentMode.RUNNER, AgentMode.SINGLE_AGENT]:
            return self.local_runner_id
        else:
            response = self.requests_session.get(
                port=self.runner_port,
                timeout=10,
                name='runner_id'
            )
            if response.status_code in [200, 400]:
                return response.json()['runner_id']
            else:
                raise Exception('Failed to get runner id')

    def send_information_report(self, _json) -> bool:
        if self.mode == AgentMode.RUNNER:
            resp = self.requests_session.post(
                port=self.proxy_port,
                json=_json,
                name='information_report'
            )
            return resp.ok
        elif self.mode in [AgentMode.PROXY, AgentMode.SINGLE_AGENT]:
            if 'usage' in _json:
                self._update_usage(_json['usage'])
            if 'monitoring' in _json:
                self.set_monitoring_status(status=_json['monitoring']['status'])
            if 'up_count' in _json:
                self._bump_monitoring_up_counter()
            return True
        else:
            raise exceptions.UnknownAgentMode('Unknown agent mode: {}'.format(self.mode))

    def send_prometheus_metrics(self, _json) -> bool:
        if self.mode == AgentMode.RUNNER:
            resp = self.requests_session.post(
                port=self.prometheus_port,
                json=_json,
                name='metrics')
            return resp.ok
        else:
            return self.handle_prometheus_update(args=_json)

    def send_execution_report(self, _json):
        if self.mode == AgentMode.RUNNER:
            self.runner_report_ws_client.send(message=_json)
        elif self.mode in [AgentMode.PROXY, AgentMode.SINGLE_AGENT]:
            self.set_execution_by_runner(execution_id=_json['execution_id'])
        else:
            raise exceptions.UnknownAgentMode('Unknown agent mode: {}'.format(self.mode))

    def get_jwt(self) -> str:
        if self.mode in [AgentMode.SINGLE_AGENT, AgentMode.PROXY]:
            self._bootstraper.login()
            return dl.token()
        elif self.mode == AgentMode.RUNNER:
            resp = self.requests_session.get(
                name='get_jwt',
                port=self.proxy_port
            )
            if resp.ok:
                return resp.json()['jwt']
            else:
                raise AssertionError('Could not get jwt from proxy')
        else:
            raise exceptions.UnknownAgentMode('Unknown agent mode: {}'.format(self.mode))

    def terminate_execution(self, execution_id: str):
        if self.mode == AgentMode.PROXY:
            payload = {'execution_id': execution_id}
            response = self.requests_session.delete(
                port=self.runner_port,
                json=payload
            )
            return response.status_code == 200, response
        else:
            if execution_id in self.executions_in_progress:
                if self.run_execution_as_process:
                    self.kill_process(execution_id=execution_id)
                else:
                    self.kill_thread(execution_id=execution_id)

    def _execution_login(self, execution_args: dict):
        user_token = execution_args.get('user_token', None)
        sdk, delete_cookie = self._get_sdk_instance(user_token=user_token)
        return sdk, delete_cookie

    def send_execution_to_runner(self, payload: dict):
        if self.mode == AgentMode.PROXY:
            self.proxy_ws_client.send(message=payload)
            res = self.proxy_ws_client.recv()
            success = json.loads(res) is True
        else:
            self.run_in_executor(args=payload)
            success = True

        return success

    #################
    # Proxy Methods #
    #################
    def append_execution(self, execution: dict, delivery_tag: str):
        self._io_handler.append_to_threads_dict(
            execution_id=execution['id'],
            delivery_tag=delivery_tag,
        )
        self.prometheus_metrics['inprogress_executions'].labels(
            serviceName=self.service.name,
            functionName=execution['functionName']).inc()

    def reset_runner(self):
        response = self.requests_session.post(
            port=self.runner_port,
            name='termination'
        )

        return response.status_code == 200, response

    def start_proxy_server(self):
        try:
            asyncio.set_event_loop(asyncio.new_event_loop())

            if self.mode == AgentMode.PROXY:
                m_server = MainWebServer(api_client=self)

                # proxy will listen only on localhost
                main_sockets = bind_sockets(
                    port=int(self.proxy_port),
                    address=self.main_address
                )
                main_server = HTTPServer(m_server)
                main_server.add_sockets(main_sockets)
                logger.info(
                    "Agent Proxy Main server is up and listening on port {}".format(self.proxy_port))

            p_server = PrometheusWebServer(api_client=self)
            prometheus_sockets = bind_sockets(port=int(self.prometheus_port))
            prometheus_server = HTTPServer(p_server)
            prometheus_server.add_sockets(prometheus_sockets)
            logger.info(
                "Agent Proxy Prometheus server is up and listening on port {}".format(self.prometheus_port))
            # start io loop
            tornado.ioloop.IOLoop.instance().start()
        except Exception:
            logger.exception('Failed starting proxy servers!')

    ##################
    # Runner Methods #
    ##################
    def send_execution_update_to_proxy(
            self,
            execution_id: str,
            status: str,
            timestamp: float,
            message: str = None,
            percent_complete: int = None,
            error: str = None,
            output=None,
            duration: float = None,
            action: str = None
    ):
        if percent_complete is None:
            percent_complete = 100 if status == 'success' else 0

        report = ExecutionStatusReport(
            service_id=self.service.id,
            execution_id=execution_id,
            replica_id=self.pod_socket_name,
            status=status,
            message=message,
            percent_complete=percent_complete,
            error=error,
            output=output,
            service_version=self.service.version,
            duration=duration,
            action=action,
            timestamp=timestamp
        )

        if self.mode in [AgentMode.SINGLE_AGENT, AgentMode.PROXY]:
            self.push_to_report_queue(report=report)
        elif self.mode == AgentMode.RUNNER:
            self.runner_status_ws_client.send(message=report.to_json())
        else:
            raise exceptions.ExecutionProgressUpdateError('[PiperReporting] - Unknown agent_mode: {}'.format(self.mode))

    def wait_for_proxy(self):
        logger.info('[Start] Waiting for Proxy')
        timeout = 60
        start = time.time()
        success = False
        while int(time.time() - start) <= timeout:
            try:
                dl.client_api.token = self.get_jwt()
                success = True
                break
            except requests.exceptions.ConnectionError:
                logger.info('[InProgress] Waiting for Proxy')
                time.sleep(1)
            except Exception:
                logger.info('[InProgress] Waiting for Proxy')
                time.sleep(1)
        if not success:
            self.termination_handler.terminate_immediately()

    @staticmethod
    def _load_new_dtlpy():
        global_cookie_file = tempfile.NamedTemporaryFile(prefix="dataloop_").name
        sdk = Dtlpy(cookie_filepath=global_cookie_file)
        return sdk

    def _get_sdk_instance(self, user_token):
        delete_cookie = False
        if user_token is not None:
            sdk = self._load_new_dtlpy()
            sdk.setenv(self.env)
            sdk.client_api.token = user_token
            if sdk.client_api.token_expired():
                logger.error('User token expired. failing..')
                raise dl.exceptions.PlatformException(error='600', message='User Token expired in package')
            delete_cookie = True
        else:
            if dl.client_api.token_expired():
                dl.client_api.token = self.get_jwt()
            sdk = dl
        sdk.client_api.refresh_token_active = False

        return sdk, delete_cookie

    def _send_response(self, execution_id, function_name, status, duration, total_duration, report):
        request_body = {
            'execution_report': {
                'execution_id': execution_id
            },
            'report': report.to_json() if report is not None else None,
            'prometheus_metrics': {
                'executionStatus': {
                    'functionName': function_name,
                    'executionStatus': status
                },
                'executionDuration': {
                    'functionName': function_name,
                    'executionStatus': status,
                    'duration': duration,
                    'total_duration': total_duration
                }
            }
        }

        for _ in range(3):
            try:
                self.send_execution_report(_json=request_body)
                break
            except Exception:
                logger.exception("Failed to notify proxy of execution completion")

    def set_service_runner(self, service_runner):
        self.service_runner = service_runner

    def _increment_execution_attempts(self, logger_header: str, execution: dict):
        try:
            # noinspection PyProtectedMember
            success, response = self.service._client_api.gen_request(
                req_type='post',
                path='/executions/{}/attempts'.format(execution['id'])
            )

            if not success:
                raise dl.exceptions.PlatformException(response)
        except dl.exceptions.BadRequest:
            operation_msg = 'Execution has reached max attempts'
            logger.error(logger_header + '[Failed] {}'.format(operation_msg))
            self.send_execution_update_to_proxy(
                execution_id=execution['id'],
                status=dl.ExecutionStatus.FAILED,
                message=operation_msg
            )
            raise exceptions.MaxAttempts()

    @property
    def _fetch_execution_inputs(self):
        # if hasattr(self.service, 'fetch_input'):
        #     return self.service.fetch_input
        return True

    def _get_resource_from_event(self, action, resource_type, resource, context):
        return resource_type is not None and resource is not None and context is not None and (
                action == 'deleted' or not self._fetch_execution_inputs
        )

    @staticmethod
    def _fetch_single_resource(value, output_type, sdk):
        if isinstance(value, dict):
            params = {'{}_id'.format(output_type.lower()): value['{}_id'.format(output_type.lower())]}
        else:
            params = {'{}_id'.format(output_type.lower()): value}

        return getattr(sdk, '{}s'.format(output_type.lower())).get(**params)

    def _parse_execution_input(
            self,
            sdk,
            input_args,
            resource_type: str = None,
            action: str = None,
            resource: dict = None,
            context: dict = None,
    ):
        inputs = dict()
        try:
            for input_arg in input_args:
                output_type = input_arg['type']
                value = input_arg['value']
                name = input_arg['name']
                if output_type.endswith('[]') and self._is_entity(output_type=output_type.replace('[]', '')):
                    output_type = output_type.replace('[]', '')
                    value = value if isinstance(value, list) else [value]
                    inputs[name] = [
                        self._fetch_single_resource(value=val, output_type=output_type, sdk=sdk) for val in value
                    ]
                elif self._is_entity(output_type=output_type):
                    if self._get_resource_from_event(
                            action=action, resource=resource, resource_type=resource_type, context=context
                    ):
                        inputs[name] = self._fetch_resource_from_event(
                            sdk=sdk,
                            resource_type=resource_type,
                            resource=resource,
                            context=context,
                        )
                    else:
                        inputs[name] = self._fetch_single_resource(value=value, output_type=output_type, sdk=sdk)
                else:
                    inputs[name] = value
        except Exception:
            del inputs
            raise
        return inputs

    @staticmethod
    def _is_entity(output_type: str):
        return output_type in [
            'Item',
            'Annotation',
            'Dataset',
            'Task',
            'Assignment',
            'Package',
            'Service',
            'Execution',
            'Trigger',
            'Project',
            'Recipe'
        ]

    def _parse_execution_output(self, function_outputs, package_outputs: str = None):
        outputs = list()
        for func_arg, package_arg in zip(function_outputs, package_outputs):
            output_type = package_arg['type']
            value = func_arg

            if output_type.endswith('[]'):
                output_type = output_type.replace('[]', '')

                if not isinstance(value, list):
                    value = [value]

                value = [
                    self._parse_entity(entity=val, output_type=output_type) if self._is_entity(
                        output_type=output_type) else val for val in value
                ]
            else:
                if self._is_entity(output_type=output_type):
                    value = self._parse_entity(entity=value, output_type=output_type)

            package_arg['value'] = value
            outputs.append(package_arg)

        return outputs

    @staticmethod
    def _fetch_resource_from_event(
            sdk,
            resource_type: str,
            resource: dict,
            context: dict = None,
    ):
        if resource_type == 'items':
            return dl.Item.from_json(_json=resource, client_api=sdk.client_api)
        elif resource_type == 'annotations':
            return dl.Annotation.from_json(_json=resource, client_api=sdk.client_api)
        elif resource_type == 'datasets':
            project = sdk.projects.get(project_id=context['project'])
            return dl.Dataset.from_json(_json=resource, client_api=sdk.client_api, project=project)
        elif resource_type == 'packages':
            project = sdk.projects.get(project_id=context['project'])
            return dl.Package.from_json(_json=resource, client_api=sdk.client_api, project=project)
        elif resource_type == 'services':
            return dl.Service.from_json(_json=resource, client_api=sdk.client_api)
        elif resource_type == 'projects':
            return dl.Project.from_json(_json=resource, client_api=sdk.client_api)
        elif resource_type == 'executions':
            return dl.Execution.from_json(_json=resource, client_api=sdk.client_api)
        elif resource_type == 'tasks':
            return dl.Task.from_json(_json=resource, client_api=sdk.client_api)
        elif resource_type == 'assignments':
            return dl.Assignment.from_json(_json=resource, client_api=sdk.client_api)
        elif resource_type == 'recipe':
            return dl.Recipe.from_json(_json=resource, client_api=sdk.client_api)
        else:
            raise exceptions.UnknownResource('Unknown resource')

    def _parse_package_input(
            self,
            sdk,
            logger_header: str,
            execution: dict,
            ident: int,
            progress: Progress,
            function_name: str,
            execution_args: dict,
            resource_type: str = None,
            action: str = None,
            resource: dict = None,
            context: dict = None,
    ) -> dict:
        self.redirect_thread_logs(
            thread_id=ident,
            execution=execution,
            function_name=function_name
        )
        try:
            run_args = self._parse_execution_input(
                sdk=sdk,
                input_args=execution_args['execution_inputs'],
                resource_type=resource_type,
                action=action,
                resource=resource,
                context=context
            )
            if self.use_user_jwt:
                run_args['dl'] = sdk
        except (sdk.exceptions.Forbidden, sdk.exceptions.Unauthorized, sdk.exceptions.NotFound):
            logger.exception(logger_header + "[Failed] - Parsing package's input")
            progress.update(status='failed', progress=0, message=traceback.format_exc())
            raise
        finally:
            self.undo_redirect_thread_logs(thread_id=ident)

        return run_args

    def _parse_package_output(
            self,
            logger_header: str,
            execution: dict,
            ident: int,
            function_name: str,
            function_outputs,
            execution_outputs
    ) -> list:
        self.redirect_thread_logs(
            thread_id=ident,
            execution=execution,
            function_name=function_name
        )
        try:
            if not isinstance(function_outputs, tuple):
                function_outputs = tuple([function_outputs])

            if len(function_outputs) != len(execution_outputs):
                output_args = [{'type': 'Any',
                                'value': function_outputs,
                                'name': 'output'}]
            else:
                output_args = self._parse_execution_output(
                    function_outputs=function_outputs,
                    package_outputs=execution_outputs
                )
        except Exception:
            logger.exception(logger_header + "[Failed] - Parsing package's output, using Any")
            output_args = [{'type': 'Any',
                            'value': function_outputs,
                            'name': 'output'}]
        finally:
            self.undo_redirect_thread_logs(thread_id=ident)

        return output_args

    @staticmethod
    def _parse_entity(entity, output_type: str):
        if isinstance(entity, dl.Annotation):
            return {'{}_id'.format(output_type.lower()): entity.id} if entity.id else entity.to_json()
        return {'{}_id'.format(output_type.lower()): entity.id if not isinstance(entity, str) else entity}

    def _parse_function_output(self, output):
        if isinstance(output, list) or isinstance(output, dl.AnnotationCollection):
            return [self._parse_function_output(o) for o in output]
        else:
            output_type = getattr(type(output), '__name__', '')
            if self._is_entity(output_type=output_type):
                return self._parse_entity(entity=output, output_type=output_type)
            return output

    def _set_process_or_thread(self, func, execution_id: str, ident: int, run_args: dict):
        if self.run_as_process:
            def process_method(kwargs, q):
                val = func(**kwargs)
                q.put(val)

            process_queue = Queue()

            p = Process(target=process_method, args=(run_args, process_queue))

            self._io_handler.set_execution_as_running(execution_id=execution_id, ident=p)
            return p, process_queue
        else:
            self._io_handler.set_execution_as_running(execution_id=execution_id, ident=ident)
            return None, None

    def _run_function(
            self,
            func,
            run_args: dict,
            ident: int,
            execution: dict,
            function_name: str,
            logger_header: str,
            p: Process = None,
            process_queue: Queue = None

    ):
        self.redirect_thread_logs(
            thread_id=ident,
            execution=execution,
            function_name=function_name
        )
        start_time = time.time()
        duration = 0

        try:
            if self.run_as_process:
                # noinspection PyUnboundLocalVariable
                p.start()
                p.join()
                retval = None if process_queue.empty() else process_queue.get()
            else:
                retval = func(**run_args)
            duration = time.time() - start_time

            if self._io_handler.check_if_process_was_killed(execution_id=execution['id']):
                raise InterruptedError('Execution was killed by user')
        except Exception:
            logger.exception(logger_header + 'Exception raised while running package.')

            # noinspection PyProtectedMember
            if hasattr(self.service_runner, '_do_reset') and self.service_runner._do_reset:
                logger.exception(
                    logger_header + 'Waiting for all executions to finish before restarting agent runner.')
                self._io_handler.set_restart(True)
            raise exceptions.PackageRuntimeException()
        finally:
            # queue clean up
            if self.run_as_process and process_queue is not None:
                while not process_queue.empty():
                    process_queue.get()
                process_queue.close()
            logger.info(self.execution_end_line)
            self.undo_redirect_thread_logs(thread_id=ident)
            self._io_handler.set_execution_as_finished(execution_id=execution['id'])

        return retval, duration

    @staticmethod
    def _cleanup(delete_cookie: bool, sdk):
        try:
            if delete_cookie and sdk is not None:
                if os.path.isfile(sdk.client_api.cookie_io.COOKIE):
                    os.remove(sdk.client_api.cookie_io.COOKIE)
                # make sure pools from sdk are delete
                # noinspection PyProtectedMember
                for name, pool in sdk.client_api._thread_pools.items():
                    pool.close()
                    pool.terminate()
        except Exception:
            logging.warning('Failed delete pools from sdk:\n{}'.format(traceback.format_exc()))

    def run_in_executor(self, args: dict):
        self.executor.submit(self._run_execution_and_report, args)

    def _run_execution_and_report(self, args: dict):
        execution_id = args['execution']['id']
        resource_type = args['resource_type']
        action = args['action']
        resource = args['resource']
        context = args['context']

        logger_header = 'executionId: {} - '.format(execution_id)
        try:
            self._io_handler.add_to_inprogress_executions(execution_id=execution_id)

            function_name, duration, status, total_duration, report = self._run_execution(
                execution_args=args,
                resource_type=resource_type,
                action=action,
                resource=resource,
                context=context
            )

            self._send_response(
                execution_id=execution_id,
                status=status,
                function_name=function_name,
                duration=duration,
                total_duration=total_duration,
                report=report
            )
        except Exception:
            logger.exception(logger_header + '[Failed] running execution inside executor')
        finally:
            try:
                self._io_handler.pop_from_inprogress_executions(execution_id=execution_id)
                if self._io_handler.is_available():
                    self.set_monitoring_status(status='running')
            except Exception:
                logger.exception('Failed in finally - _run_execution_and_report()')

    def get_function(self, function_name: str):
        func = getattr(self.service_runner, function_name)

        if function_name in self.functions_params_check:
            need_progress = self.functions_params_check[function_name]['progress']
            need_context = self.functions_params_check[function_name]['context']
        else:
            params = list(signature(func).parameters)
            need_progress = "progress" in params
            need_context = "context" in params
            self.functions_params_check[function_name] = dict(progress=need_progress, context=need_context)

        return func, need_progress, need_context

    def _run_execution(
            self,
            execution_args,
            resource_type,
            action,
            resource,
            context
    ):
        progress = delete_cookie = sdk = None
        logger_header = function_name = ''
        ident = threading.get_ident()
        start_time = time.time()
        duration = 0
        total_duration = 0
        status = 'failed'
        report = None

        try:
            logger.info('[Start] {}'.format('Execution Started.'))
            execution_id = execution_args['execution']['id']
            logger_header = 'executionId: {} - '.format(execution_id)

            sdk, delete_cookie = self._execution_login(execution_args=execution_args)

            function_name = execution_args['execution']['functionName']

            progress = Progress(api_client=self, execution=execution_args['execution'])

            run_args = self._parse_package_input(
                sdk=sdk,
                logger_header=logger_header,
                execution=execution_args['execution'],
                ident=ident,
                progress=progress,
                function_name=function_name,
                execution_args=execution_args,
                resource_type=resource_type,
                action=action,
                resource=resource,
                context=context
            )

            progress.update(status='in-progress', progress=0)

            func, need_progress, need_context = self.get_function(function_name=function_name)

            if need_progress:
                run_args['progress'] = progress

            if need_context and 'context' not in run_args:
                run_args['context'] = dl.Context(
                    project=self.project,
                    service=self.service,
                    package=self.package,
                    execution_dict=execution_args['execution'],
                    event_context=execution_args.get('event_context', dict()),
                    logger=progress.logger,
                    progress=progress,
                    sdk=sdk
                )

            p, process_queue = self._set_process_or_thread(
                func=func,
                execution_id=execution_id,
                ident=ident,
                run_args=run_args
            )

            output, duration = self._run_function(
                p=p,
                func=func,
                ident=ident,
                run_args=run_args,
                execution=execution_args['execution'],
                function_name=function_name,
                logger_header=logger_header,
                process_queue=process_queue
            )

            # output = self._parse_package_output(
            #     logger_header=logger_header,
            #     execution=execution,
            #     ident=ident,
            #     function_name=function_name,
            #     function_outputs=output,
            #     execution_outputs=execution_args.get('execution_outputs', list())
            # )

            output = self._parse_function_output(output=output)

            status = 'success'
            timestamp = progress.get_timestamp()

            report = ExecutionStatusReport(
                service_id=self.service.id,
                execution_id=execution_id,
                replica_id=self.pod_socket_name,
                status=status,
                percent_complete=100,
                output=output,
                service_version=self.service.version,
                duration=duration,
                action=action,
                timestamp=timestamp
            )

        except Exception:
            end_time = time.time()
            duration = end_time - start_time

            logger.exception(logger_header + 'Exception raised while processing execution.')
            message = '{}'.format(traceback.format_exc())
            report = ExecutionStatusReport(
                service_id=self.service.id,
                execution_id=execution_args['execution']['id'],
                replica_id=self.pod_socket_name,
                status='failed',
                percent_complete=progress.progress if progress is not None else 0,
                output=None,
                service_version=self.service.version,
                duration=duration,
                action=action,
                message=message,
                error=message,
                timestamp=progress.get_timestamp() if progress is not None else (time.time() * 1000)
            )

        finally:
            try:
                if self._io_handler.need_restart():
                    self._io_handler.restart_runner()
                self._cleanup(delete_cookie=delete_cookie, sdk=sdk)
                total_duration = self._get_total_duration(
                    total_duration=total_duration,
                    created_at=execution_args.get('execution', dict()).get('createdAt', None)
                )
            except Exception:
                logger.exception('Failed in finally - _run_execution()')

        return function_name, duration, status, total_duration, report

    @staticmethod
    def _get_total_duration(total_duration=0, created_at: str = None):
        if created_at:
            try:
                total_duration = time.time() - dateutil.parser.isoparse(created_at).timestamp()
            except Exception:
                logger.exception('Failed to calculate total duration')

        return total_duration
