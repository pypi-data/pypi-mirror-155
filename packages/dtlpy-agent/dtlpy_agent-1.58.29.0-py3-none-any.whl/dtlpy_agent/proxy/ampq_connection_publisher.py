from threading import Thread
from typing import Union
import amqpstorm
import time
import logging
import json
import os
from queue import Empty

from dtlpy_agent.exceptions import ReportSerializationError

logger = logging.getLogger(name='AgentProxy.mq_connection.publisher')


class ReportType:
    SERVICE_STATUS = 'serviceStatus'
    EXECUTION_STATUS = 'executionStatus'


class Report:
    def __init__(
            self,
            report_type: str,
            service_id: str,
            replica_id: str,
            timestamp: float = None
    ):
        self.report_type = report_type
        self.service_id = service_id
        self.replica_id = replica_id

        if timestamp is None:
            timestamp = time.time() * 1000
        self.timestamp = timestamp

    @staticmethod
    def _validate_serialization(_json: dict):
        try:
            json.dumps(_json)
        except Exception:
            raise ReportSerializationError('[PiperReporting] - Report is not json serializable')

    def to_json(self):
        _json = dict(
            reportType=self.report_type,
            serviceId=self.service_id,
            replicaId=self.replica_id,
            timestamp=self.timestamp
        )

        return _json


class ServiceStatusReport(Report):
    def __init__(
            self,
            service_id: str,
            replica_id: str,
            status: str,
            num_restarts: int,
            uptime: float = 0

    ):
        super(ServiceStatusReport, self).__init__(
            report_type=ReportType.SERVICE_STATUS,
            service_id=service_id,
            replica_id=replica_id
        )
        self.status = status
        self.uptime = uptime
        self.num_restarts = num_restarts

    def to_json(self):
        _json = super().to_json()

        _json.update(
            status=self.status,
            uptime=self.uptime,
            numRestarts=self.num_restarts
        )

        self._validate_serialization(_json=_json)

        return _json


class ExecutionStatusReport(Report):
    def __init__(
            self,
            service_id: str,
            replica_id: str,
            execution_id: str,
            status: str,
            percent_complete: int,
            output,
            service_version: str,
            error: str = None,
            message: str = None,
            duration: float = None,
            action: str = None,
            timestamp: float = None
    ):
        super(ExecutionStatusReport, self).__init__(
            report_type=ReportType.EXECUTION_STATUS,
            service_id=service_id,
            replica_id=replica_id,
            timestamp=timestamp
        )
        self.execution_id = execution_id
        self.status = status
        self.message = message
        self.percent_complete = percent_complete
        self.error = error
        self.output = output
        self.service_version = service_version
        self.duration = duration
        self.action = action
        self.update_item = True

    @staticmethod
    def from_json(_json: dict):
        return ExecutionStatusReport(
            service_id=_json.get('serviceId', None),
            replica_id=_json.get('replicaId', None),
            execution_id=_json.get('executionId', None),
            status=_json.get('status', None),
            message=_json.get('message', None),
            percent_complete=_json.get('percentComplete', None),
            error=_json.get('error', None),
            output=_json.get('output', None),
            service_version=_json.get('serviceVersion', None),
            duration=_json.get('duration', None),
            action=_json.get('action', None),
            timestamp=_json.get('timestamp', None)
        )

    def to_json(self):
        _json = super().to_json()

        _json.update(
            executionId=self.execution_id,
            status=self.status,
            message=self.message,
            percentComplete=self.percent_complete,
            error=self.error,
            output=self.output,
            serviceVersion=self.service_version,
            updateItem=self.update_item
        )

        if self.duration is not None:
            _json.update(duration=self.duration)

        if self.action is not None:
            _json.update(action=self.action)

        self._validate_serialization(_json=_json)

        return _json


class RabbitMqPublisherClient(Thread):
    def __init__(
            self,
            api_client,
            hostname: str,
            username: str,
            password: str
    ):
        super(RabbitMqPublisherClient, self).__init__()
        self._api_client = api_client
        self._hostname = hostname
        self._username = username
        self._password = password

        self._stopped = False

        env_for_exchange = api_client.env

        if env_for_exchange == 'dev':
            env_for_exchange = 'dev'
        elif env_for_exchange == 'prod':
            env_for_exchange = 'production'
        elif env_for_exchange == 'rc':
            env_for_exchange = 'rc'
        else:
            minikube_env = os.environ.get('MINIKUBE_ENV_NAME')
            env_for_exchange = minikube_env if minikube_env is not None else env_for_exchange

        self._report_exchange = os.environ.get(
            'PIPER_REPORTING_EXCHANGE',
            'piper-reporting-queue-{}'.format(env_for_exchange)
        )
        self._service_status_report_rout = os.environ.get(
            'SERVICE_STATUS_REPORT_ROUT',
            'service-status'
        )
        self._execution_status_report_rout = os.environ.get(
            'EXECUTION_STATUS_REPORT_ROUT',
            'execution-status'
        )

    @property
    def _service_status_queue_name(self):
        return '{}-{}'.format(self._report_exchange, self._service_status_report_rout)

    @property
    def _execution_status_queue_name(self):
        return '{}-{}'.format(self._report_exchange, self._execution_status_report_rout)

    def stop(self):
        self._stopped = True

    def _get_message(self) -> Union[ServiceStatusReport, ExecutionStatusReport]:
        return self._api_client.get_from_report_queue()

    def _return_message_to_queue(self, report: Union[ServiceStatusReport, ExecutionStatusReport]):
        try:
            return self._api_client.push_to_report_queue(report=report)
        except Exception:
            logger.exception('[PiperReporting] - Failed to return message to queue')

    def _get_routing_key(self, report: Union[ServiceStatusReport, ExecutionStatusReport]):
        if report.report_type == ReportType.SERVICE_STATUS:
            return self._service_status_report_rout
        elif report.report_type == ReportType.EXECUTION_STATUS:
            return self._execution_status_report_rout

    @property
    def hostname(self):
        hostname, _ = self._hostname.split('/')
        return hostname

    @property
    def virtual_host(self):
        _, v_host = self._hostname.split('/')
        return v_host

    @property
    def get_mq_connection_credentials(self) -> dict:
        if self._api_client.env in ['local', 'minikube_local_mac']:
            return dict(
                hostname=self.hostname.split('/')[0],
                port=5672,
                username='guest',
                password='guest',
                virtual_host='rabbitmq',
                ssl=False
            )
        else:
            return dict(
                hostname=self.hostname,
                username=self._username,
                password=self._password,
                virtual_host=self.virtual_host
            )

    def run(self):
        while True:
            try:
                with amqpstorm.Connection(**self.get_mq_connection_credentials) as connection:
                    with connection.channel() as channel:
                        while not self._stopped:
                            try:
                                report = self._get_message()
                                routing_key = self._get_routing_key(report=report)
                                message = amqpstorm.Message.create(
                                    channel,
                                    body='{}'.format(json.dumps(report.to_json())),
                                    properties={
                                        'content_type': 'application/json'
                                    })
                                message.publish(
                                    exchange=self._report_exchange,
                                    routing_key=routing_key
                                )
                            except ReportSerializationError:
                                logger.exception('[PiperReporting] - Failed to publish report to piper reporting queue')
                            except Empty:
                                logger.exception('[PiperReporting] - Timeout received while getting message from queue')
            except Exception:
                logger.exception('[PiperReporting] - Publisher failed - reconnecting to RabbitMQ.')
