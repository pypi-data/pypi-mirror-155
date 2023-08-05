import dtlpy as dl
import threading
import datetime
import logging
import psutil
import time

from dtlpy_agent.proxy.ampq_connection_publisher import ServiceStatusReport

logger = logging.getLogger(name='AgentProxy.Usage')


class TimeSeriesMonitoring(threading.Thread):
    def __init__(self,
                 project: dl.entities.Project,
                 service: dl.entities.Service,
                 pod_socket_name: str,
                 api_client,
                 ):
        threading.Thread.__init__(self)
        self.api_client = api_client
        self.interval = 60
        self.project = project
        self.service = service
        self.pod_socket_name = pod_socket_name
        self.cpu = -1
        self.ram = -1
        self.last_delete = None
        self.runtime_time_series = None
        self.system_time_series = None
        self.sample_id = None

    def setup(self):
        self.runtime_time_series = TimeSeriesMonitoring.get_first_time_series(
            project=self.project,
            ts_name='DeploymentsRuntime'
        )

        self.system_time_series = TimeSeriesMonitoring.get_first_time_series(
            project=self.project,
            ts_name='DeploymentsSystemInformation'
        )

        try:
            org_id = self.project.org['id']
        except Exception:
            org_id = 'null'

        instance_type = self.service.runtime if isinstance(self.service.runtime,
                                                           dict) else self.service.runtime.to_json()
        samples_ids = self.runtime_time_series.add_samples(
            data={
                'uptime': self.get_time(),
                'downtime': self.get_time(),
                'serviceId': self.service.id,
                'podId': self.pod_socket_name,
                'projectId': self.project.id,
                'orgId': org_id,
                'instanceType': instance_type
            }
        )
        self.sample_id = samples_ids[0]['id']

    @staticmethod
    def get_time():
        return int(datetime.datetime.utcnow().timestamp() * 1000)

    def set_report(self, report: dict):
        self.cpu = report['cpu']
        self.ram = report['ram']

    def update_uptime(self):
        self.runtime_time_series.update_sample(
            sample_id=self.sample_id,
            data={
                'downtime': self.get_time()
            }
        )

    def update_system_information(self):
        sample = dl.ServiceSample(
            start_time=time.time() * 1000,
            end_time=time.time() * 1000,
            user_id=dl.info()['user_email'],
            project_id=self.project.id,
            org_id=self.project.org['id'],
            service_id=self.service.id,
            pod_id=self.pod_socket_name,
            pod_type=self.service.runtime.pod_type,
            event_type='service',
            entity_type='service',
            action='activity',
            cpu=psutil.Process().cpu_percent(5),
            ram=psutil.Process().memory_info().rss,
            status=self.api_client.monitoring.status
        )
        num_tries = 3
        for i in range(num_tries):
            try:
                self.project.analytics.report_metrics([sample])
            except Exception as e:
                logger.debug('Failed to upload sample trial: {}/{}'.format(i, num_tries))
                logger.exception('Failed to upload sample. Data: {}'.format(sample))


    def run(self):

        setup_success = False
        while not setup_success:
            try:
                self.setup()
                setup_success = True
            except Exception:
                logger.warning('Failing to setup proxy usage')
                time.sleep(60)

        while True:
            try:
                if dl.token_expired():
                    self.api_client.get_jwt()
                self.update_uptime()
            except Exception:
                logger.exception('Failed to update uptime timeseries')
            finally:
                time.sleep(self.interval)

            try:
                if dl.token_expired():
                    self.api_client.get_jwt()
                self.update_system_information()
            except Exception:
                logger.exception('Failed to update system information timeseries')
            finally:
                time.sleep(self.interval)

    @staticmethod
    def get_first_time_series(project, ts_name):
        ts = None
        for i in range(3):
            try:
                # get existing time series
                time_series = [ts for ts in project.times_series.list() if ts.name == ts_name]
                if len(time_series) == 0:
                    raise Exception('Time series not found')
                elif len(time_series) > 1:
                    logger.info('[{}] - More than one time series found, selecting oldest one.'.format(ts_name))
                    ts = time_series[0]
                    for single_time_series in time_series:
                        if single_time_series.createdAt < ts.createdAt:
                            ts = single_time_series
                else:
                    ts = time_series[0]
                    logger.info('[{}] - Time series found: {}'.format(ts_name, ts.id))
            except Exception:
                logger.info('[{}] - Time series not found. Creating new time series.'.format(ts_name))
                try:
                    ts = project.times_series.create(series_name=ts_name)
                    logger.info('[{}] - Time series created: {}'.format(ts_name, ts.id))
                except Exception:
                    logger.exception('[{}] - Failed to create time series'.format(ts_name))
                    ts = None
            if ts is not None:
                break

        if ts is None:
            raise Exception('Failed to get time series')

        return ts


class Monitoring(threading.Thread):
    def __init__(
            self,
            project: dl.entities.Project,
            service: dl.entities.Service,
            pod_socket_name: str,
            tic_uptime,
            api_client
    ):
        threading.Thread.__init__(self)
        self.interval = 10
        self.project = project
        self.service = service
        self.pod_socket_name = pod_socket_name
        self.status = 'initializing'
        self.up_counter = -1
        self.tic_uptime = tic_uptime
        self.toc_uptime = None
        self.uptime = None
        self.api_client = api_client

    def set_status(self, value: str):
        self.status = value

    def bump_up_counter(self):
        self.up_counter += 1

    def update(self):
        num_tries = 3
        report = ServiceStatusReport(
            service_id=self.service.id,
            replica_id=self.pod_socket_name,
            num_restarts=self.up_counter,
            status=self.status
        )

        if self.toc_uptime is None:
            if self.status == 'running':
                self.toc_uptime = time.time()
                self.uptime = self.toc_uptime - self.tic_uptime

        if self.uptime is not None:
            report.uptime = self.uptime

        for i in range(num_tries):
            try:
                self.api_client.update_service_status(report=report)
            except Exception:
                logger.exception(
                    'Failed to upload sample trial: {}/{}. Data: {}'.format(
                        i, num_tries, report.to_json()
                    )
                )

    def run(self):
        while True:
            try:
                if dl.token_expired(t=60):
                    self.api_client.get_jwt()
                self.update()
                self.api_client.reset_monitoring_status()
            except Exception:
                logger.exception('Failed update status to platform')
            finally:
                time.sleep(self.interval)
