import threading
import logging
import psutil
import time

logger = logging.getLogger(name='AgentRunner.Usage')


class RunnerMonitoring(threading.Thread):
    def __init__(self, client_api):
        threading.Thread.__init__(self)
        self.client_api = client_api
        try:
            self.interval = int(client_api.get_information_interval() / 2)
        except Exception:
            logger.exception("Failed get interval from proxy:")
            self.interval = 1
        self.status = 'initializing'

    @staticmethod
    def usage() -> dict:
        usage = {
            'usage': {
                'cpu': psutil.Process().cpu_percent(3),
                'ram': psutil.Process().memory_info().rss
            }
        }
        return usage

    def report_timeseries_system_information(self):
        usage = self.usage()
        success = self.client_api.send_information_report(_json=usage)
        if not success:
            logger.exception("Failed to notify proxy system in formation:")

    def report_prometheus_system_information(self):
        usage = self.usage()
        metrics = {'memoryCpuUsage': usage['usage']}
        success = self.client_api.send_prometheus_metrics(_json=metrics)
        if not success:
            logger.exception("Failed to notify prometheus system in formation:")

    def report_up(self):
        reports = {'up_count': dict()}
        success = self.client_api.send_information_report(_json=reports)
        if not success:
            logger.exception("Failed update up counter")

    def report_monitoring(self):

        if self.client_api.is_runner_full():
            status = 'full'
        else:
            status = self.status

        reports = {'monitoring': {'status': status}}
        success = self.client_api.send_information_report(_json=reports)
        if not success:
            logger.exception("Failed to notify proxy system in formation:")

    def run(self):
        while True:
            try:
                self.report_monitoring()
            except Exception:
                logger.exception('Failed update status information')

            try:
                self.report_prometheus_system_information()
            except Exception:
                logger.exception('Failed update prometheus system information')

            try:
                self.report_timeseries_system_information()
            except Exception:
                logger.exception('Failed update time series system information')

            time.sleep(self.interval)

    def set_status(self, value):
        if isinstance(value, str):
            self.status = value
        else:
            logger.exception('Failed update status, status is unvalid')
