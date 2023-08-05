import time
import dtlpy as dl
import json
import logging

main_logger = logging.getLogger(name='AgentRunner.Progress')
main_logger.setLevel(logging.DEBUG)


class Progress(dl.Progress):

    def __init__(self, api_client, execution: dict):
        self._api_client = api_client
        self.execution_id = execution['id']
        self.function_name = execution['functionName']
        self.progress = 0
        self.status = execution['latestStatus'].get('status', 'created')
        self.logger = main_logger
        self.timestamp_addition = 0

    @staticmethod
    def is_json_serializable(_json):
        try:
            json.dumps(_json)
            return True
        except Exception:
            main_logger.exception('Output is not json serializable')
            main_logger.debug(_json)
            return False

    def need_update(
            self,
            status=None,
            progress=None,
            message=None,
            output=None,
            action=None
    ):
        only_progress = (status is None or status == self.status) and all(v is None for v in [message, output, action])
        progress_changed = progress is not None and (
                (progress == 100 and self.progress < 100) or progress >= self.progress + 5
        )
        return progress_changed if only_progress else True

    def update(
            self,
            status=None,
            progress=None,
            message=None,
            output=None,
            duration=None,
            action=None
    ):
        if self.need_update(
                status=status,
                progress=progress,
                message=message,
                output=output,
                action=action
        ):
            status = self.status = self.status if status is None else status

            if progress is not None:
                self.progress = max(min(progress, 100), self.progress)

            self.update_execution(
                message=message,
                output=output if self.is_json_serializable(_json=output) else dict(),
                duration=duration,
                status=status,
                progress=self.progress,
                action=action
            )

    def get_timestamp(self):
        timestamp = (time.time() * 1000) + self.timestamp_addition
        self.timestamp_addition = self.timestamp_addition + 1
        return timestamp

    def update_execution(self, status, message, output, duration, progress, action=None):
        try:
            timestamp = self.get_timestamp()
            self._api_client.send_execution_update_to_proxy(
                execution_id=self.execution_id,
                status=status,
                percent_complete=progress,
                message=message,
                output=output,
                duration=duration,
                action=action,
                timestamp=timestamp
            )
        except Exception:
            main_logger.exception('[Progress] - Failed to update execution progress: {}'.format(self.execution_id))
