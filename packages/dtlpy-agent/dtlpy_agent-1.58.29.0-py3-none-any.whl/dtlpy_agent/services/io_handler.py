from multiprocessing import Lock, Process
from typing import Union
import logging
import signal
import os
import time
import queue

from dtlpy_agent.proxy.ampq_connection import Consumer
from dtlpy_agent.proxy.ampq_connection_publisher import ServiceStatusReport, ExecutionStatusReport

logger = logging.getLogger('AgentRunner.IOhandler')


class IOHandler:
    def __init__(self):
        # runner io
        self.queue = 0
        self.num_workers = 32  # default - to be set in load_package
        self.restart = False
        self.runner_id_lock = Lock()
        self.restart_lock = Lock()
        self.run_execution_as_process = False
        self.executions_in_progress = dict()
        self.thread_ids_to_logging_dict = dict()
        self.user_log_phrase = 'DTLPYFLUENTDUSERLOGPHRASE'
        self.killed_execution_process_list = list()
        self.killed_execution_process_list_lock = Lock()
        self._runner_is_up = False
        self._mq = None

        # proxy io
        self._threads_dict = dict()
        self._threads_dict_lock = Lock()
        self.usage_interval = 5
        self.monitoring_interval = 5

        # shared attributes
        self._runner_id = None

        # service id for logs
        self._service_id = None

        # project id for logs
        self._project_id = None

        # reporting queue
        self._report_queue = queue.Queue()

    def get_from_report_queue(self) -> Union[ServiceStatusReport, ExecutionStatusReport]:
        return self._report_queue.get()

    def push_to_report_queue(self, report: Union[ServiceStatusReport, ExecutionStatusReport]):
        return self._report_queue.put(report)

    @property
    def queue_empty(self):
        return self._report_queue.empty()

    def get_report_queue_size(self):
        return self._report_queue.qsize()

    @property
    def service_id(self):
        if self._service_id is None:
            self._service_id = os.environ.get('SERVICE_ID', None)
        return self._service_id

    def set_service_id(self, service_id: str):
        self._service_id = service_id

    @property
    def project_id(self):
        return self._project_id

    def set_project_id(self, project_id: str):
        self._project_id = project_id

    def get_runner_id(self) -> str:
        with self.runner_id_lock:
            return self._runner_id

    def add_thread_to_logging(
            self,
            thread_id: int,
            function_name: str,
            execution_id: str,
            system: bool = False,
            pipeline_id: str = None,
            pipeline_execution_id: str = None,
            node_id: str = None,
            project_id: str = None
    ):
        self.thread_ids_to_logging_dict[thread_id] = {
            "function_name": function_name,
            "execution_id": execution_id,
            "service_id": self.service_id,
            "system": system,
            "fluentd_filter_key": self.user_log_phrase,
            "pipeline_id": pipeline_id or '',
            "node_id": node_id or '',
            "pipeline_execution_id": pipeline_execution_id or '',
            "project_id": project_id
        }

    @property
    def _system_log_object(self) -> dict:
        return {
            "function_name": 'system',
            "execution_id": '',
            "service_id": self.service_id,
            "system": True,
            "fluentd_filter_key": self.user_log_phrase,
            "project_id": self.project_id
        }

    def pop_thread_from_logging(self, thread_id: int):
        self.thread_ids_to_logging_dict.pop(thread_id)

    def get_header(self, thread_id: int) -> dict:
        line_header = self.thread_ids_to_logging_dict.get(thread_id, False)
        if not line_header:
            line_header = self._system_log_object
        return line_header

    def set_restart(self, restart: bool):
        with self.restart_lock:
            self.restart = restart

    @property
    def mq(self):
        if self._mq:
            assert isinstance(self._mq, Consumer)
            return self._mq

    @mq.setter
    def mq(self, val: Consumer):
        self._mq = val

    def set_runner_id(self, runner_id: str):
        with self.runner_id_lock:
            self._runner_id = runner_id

    def runner_started(self):
        self._runner_is_up = True

    @property
    def is_full(self) -> bool:
        return self.num_inprogress >= self.num_workers

    @property
    def intervals(self) -> dict:
        intervals = {
            'usage_interval': self.usage_interval,
            'monitoring_interval': self.monitoring_interval
        }
        return intervals

    def is_available(self) -> bool:
        return self._runner_is_up and not self.restart

    def queue_is_empty(self) -> bool:
        return self.num_inprogress <= 0

    @property
    def num_inprogress(self) -> int:
        return len(self.executions_in_progress)

    def need_restart(self) -> bool:
        return self.restart

    def get_execution_ident(self, execution_id: str):
        return self.executions_in_progress.get(execution_id, None)

    #########################################################
    # running and in progress executions dictionary handling #
    #########################################################
    def add_to_inprogress_executions(self, execution_id: str):
        self.executions_in_progress[execution_id] = -1

    def set_execution_as_running(self, execution_id: str, ident: Union[int, Process]):
        self.executions_in_progress[execution_id] = ident

    def set_execution_as_finished(self, execution_id: str):
        self.executions_in_progress[execution_id] = -1

    def pop_from_inprogress_executions(self, execution_id: str):
        self.executions_in_progress.pop(execution_id, None)

    #############
    # kill list #
    #############
    def add_to_killed_process_list(self, execution_id: str):
        with self.killed_execution_process_list_lock:
            self.killed_execution_process_list.append(execution_id)

    def check_if_process_was_killed(self, execution_id: str) -> bool:
        if execution_id in self.killed_execution_process_list:
            with self.killed_execution_process_list_lock:
                try:
                    self.killed_execution_process_list.remove(execution_id)
                except Exception:
                    pass
            return True
        else:
            return False

    def kill_thread(self, execution_id: str, service_runner):
        logger.info('Thread kill order was received from proxy for execution: {}'.format(execution_id))
        try:
            logger.info('[START] Notified service_runner to kill thread for execution: {}'.format(execution_id))
            # noinspection PyProtectedMember
            service_runner._terminate(tid=self.get_execution_ident(execution_id=execution_id))
            logger.info('[DONE] Notified service_runner to kill thread for execution: {}'.format(execution_id))
        except Exception:
            logger.exception('[FAILED] Notified service_runner to kill thread')

    def kill_process(self, execution_id: str):
        logger.info('Process kill order was received from proxy')
        try:
            logger.info('[START] Killing process of execution: {}'.format(execution_id))
            process = self.get_execution_ident(execution_id=execution_id)
            self.add_to_killed_process_list(execution_id=execution_id)
            os.kill(process.ident, signal.SIGKILL)
            logger.info('[DONE] Killing process of execution: {}'.format(execution_id))
        except Exception:
            logger.exception('[FAILED] Killing process')

    def restart_runner(self):
        logger.debug('In restart agent runner. num executions in progress: {}'.format(self.num_inprogress))
        if self.queue_is_empty():
            logger.warning('All executions completed, restarting agent runner!')
            # noinspection PyProtectedMember
            os._exit(os.EX_OSERR)

    def is_active_execution(self, execution_id) -> bool:
        val = self._threads_dict.get(execution_id, None)
        return val is not None

    def remaining_executions(self) -> int:
        return len(self._threads_dict)

    def executions_snapshot(self) -> dict:
        val = dict()
        with self._threads_dict_lock:
            val.update(self._threads_dict)
        return {key: val['start_time'] for key, val in val.items()}

    def append_to_threads_dict(self, execution_id: str, delivery_tag: str):
        with self._threads_dict_lock:
            self._threads_dict[execution_id] = {
                'runner_id': self._runner_id,
                'set_by_runner': True,
                'start_time': time.time(),
                'delivery_tag': delivery_tag
            }

    def set_execution_by_runner(self, execution_id: str):
        execution = self.pop_from_proxy_execution(execution_id=execution_id)
        if execution:
            self.mq.ack(execution['delivery_tag'])

    def execution_runner_was_reset(self, execution_id: str) -> bool:
        try:
            return not self._threads_dict[execution_id]['set_by_runner']
        except Exception:
            return False

    def pop_from_proxy_execution(self, execution_id: str):
        return self._threads_dict.pop(execution_id, None)

    def set_execution_by_reset(self, execution_id: str):
        try:
            execution = self.pop_from_proxy_execution(execution_id=execution_id)
            self.mq.nack(execution['delivery_tag'])
        except Exception:
            logger.warning('Failed to set execution by reset: {}'.format(execution_id))

    def set_execution_by_reset_without_lock(self, execution_id: str):
        try:
            execution = self.pop_from_proxy_execution(execution_id=execution_id)
            execution['set_by_runner'] = False
            self.mq.nack(execution['delivery_tag'])
        except Exception:
            logger.warning('Failed to set execution: {}'.format(execution_id))

    def handle_runner_reset(self, force_all: bool = False):
        logger.debug('Handling runner reset')
        with self._threads_dict_lock:
            executions = list(self._threads_dict.keys())
            for execution in executions:
                if force_all or self._threads_dict[execution]['runner_id'] != self._runner_id:
                    logger.debug('Releasing execution: {}'.format(execution))
                    self.set_execution_by_reset_without_lock(execution_id=execution)
