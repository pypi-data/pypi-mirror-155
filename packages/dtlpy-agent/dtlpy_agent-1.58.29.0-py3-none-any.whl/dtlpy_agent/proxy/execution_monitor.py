import threading
import logging
import time
import dtlpy as dl

logger = logging.getLogger(name='AgentProxy.ExecutionsMonitoring')


class ExecutionMonitor(threading.Thread):
    def __init__(self, api_client, service, interval=120):
        threading.Thread.__init__(self)
        self.api_client = api_client
        self.interval = interval
        self.service = service
        self.has_timeout = service.execution_timeout is not None and service.execution_timeout > 0

    def check_executions(self):
        executions_start_time_dict = self.api_client.executions_snapshot()
        for execution_id, execution_start_time in executions_start_time_dict.items():
            if self.has_timeout and (time.time() - execution_start_time) > self.service.execution_timeout:
                logger.warning(
                    'Execution: {} has reached its timeout. Starting termination procedure'.format(execution_id))
                self.api_client.termination_handler.proxy_termination_handler()
            execution = dl.executions.get(execution_id=execution_id)
            if execution.to_terminate:
                logger.warning('Execution: {} received a termination request'.format(execution_id))
                self.kill_execution(execution_id=execution_id)
                logger.warning('[DONE]- Terminating execution: {}'.format(execution_id))

    def stop_consuming(self):
        self.api_client.stop_consuming()
        logger.warning('Stopped consuming')

    def _get_remaining_executions(self, trigger_execution_id: str):
        executions_dict: dict = self.api_client.executions_snapshot()
        return [e for e in executions_dict.keys() if e != trigger_execution_id]

    def kill_execution(self, execution_id):
        success, _ = self.api_client.terminate_execution(execution_id=execution_id)
        if success:
            logger.info('Termination request for execution: {} was sent successfully to runner')
        else:
            logger.error('Termination request for execution: {} failed')

    def run(self):
        while True:
            try:
                if dl.token_expired():
                    self.api_client.get_jwt()
                self.check_executions()
            except Exception:
                logger.exception('Failed to monitor executions')
            finally:
                time.sleep(self.interval)
