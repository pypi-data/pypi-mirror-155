import time
import logging
from multiprocessing import Lock
import dtlpy as dl
import os

logger = logging.getLogger(__name__)


class TerminationHandler:
    def __init__(self, client_api):
        self.client_api = client_api
        self._termination_started = False
        self._termination_started_lock = Lock()

    def check_if_terminating(self):
        self._termination_started_lock.acquire()
        need_to_terminate = not self._termination_started
        self._termination_started = True
        self._termination_started_lock.release()
        return need_to_terminate

    def runner_termination_handler(self):
        need_to_terminate = self.check_if_terminating()
        if need_to_terminate:
            self.client_api.set_monitoring_status(status='terminating')
            self.client_api.set_restart(True)

            while not self.client_api.queue_is_empty():
                logger.info(
                    "[SHUTTING DOWN] {} remaining execution.".format(
                        self.client_api.num_inprogress_executions
                    )
                )
                time.sleep(3)

            logger.info("[SHUTTING DOWN] all executions completed.")
            logger.info("[SHUTTING DOWN] waiting for 'termination' from proxy")

    @staticmethod
    def terminate_immediately():
        # noinspection PyUnresolvedReferences,PyProtectedMember
        os._exit(os.EX_OSERR)

    def proxy_termination_handler(self):
        need_to_terminate = self.check_if_terminating()
        if need_to_terminate:
            self.client_api.stop_consuming()
            self.client_api.set_monitoring_status(status='terminating')
            executions_start_time_dict = self.client_api.executions_snapshot()

            if self.client_api.service.execution_timeout is not None and self.client_api.service.execution_timeout > 0:
                timeout = self.client_api.service.execution_timeout
            else:
                timeout = float('inf')

            while len(executions_start_time_dict) > 0:
                now = time.time()
                for execution_id, start in executions_start_time_dict.items():
                    runtime = now - start
                    if runtime > timeout:
                        self._ack_nack_timeout_execution(
                            on_reset=self.client_api.service.on_reset,
                            execution_id=execution_id
                        )
                logger.info("[SHUTTING DOWN] {} remaining execution. ids: {}".format(len(executions_start_time_dict),
                                                                                     list(executions_start_time_dict.keys())))
                time.sleep(3)
                executions_start_time_dict = self.client_api.executions_snapshot()

            self._reset_runner()

            while not self.client_api.reporting_queue_empty:
                logger.info(
                    "[SHUTTING DOWN] - [PiperReporting] There are remaining report messages in queue: {}".format(
                        self.client_api.get_report_queue_size()
                    )
                )
                time.sleep(2)

            logger.info("[SHUTTING DOWN] all report messages were sent to piper. shutting down")

            self.terminate_immediately()

    def _reset_runner(self):
        success = False
        for i in range(3):
            try:
                success, _ = self.client_api.reset_runner()
            except Exception:
                success = False
            if success:
                break
        if success:
            logger.info('[Done] Runner restart')
        else:
            logger.critical('[Failed] Runner restart')

    def _ack_nack_timeout_execution(self, on_reset: str, execution_id: str):
        if self.client_api.is_active_execution(execution_id=execution_id):
            dl.executions.progress_update(
                execution_id=execution_id,
                status=on_reset,
                message='{} due to runner timeout'.format(on_reset.capitalize())
            )
        if on_reset == 'failed':
            self.client_api.set_execution_by_runner(execution_id=execution_id)
        elif on_reset == 'rerun':
            self.client_api.set_execution_by_reset(execution_id=execution_id)
        else:
            logger.error('Unknown "on_reset" operation: {!r}. setting to failed'.format(on_reset))
            self.client_api.set_execution_by_runner(execution_id=execution_id)
