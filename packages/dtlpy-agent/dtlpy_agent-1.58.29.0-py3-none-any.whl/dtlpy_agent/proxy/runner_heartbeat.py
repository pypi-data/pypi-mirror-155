import logging
import threading
import time

from .. import exceptions

logger = logging.getLogger(name='AgentProxy.RunnerHeartbeat')


class RunnerHeartbeat(threading.Thread):

    def __init__(self, api_client):
        threading.Thread.__init__(self)
        self.api_client = api_client
        self.num_tries = 5
        self.heartbeat_time = 60

    def get_runner_id(self):
        runner_id = None
        success = False

        for i in range(self.num_tries):
            try:
                runner_id = self.api_client.get_runner_id()
                success = True
                break
            except Exception:
                logger.warning('[Runner Heartbeat] Runner is NOT available. Trial: {}/{}'.format(i, self.num_tries))
                time.sleep(1)

        if success:
            return runner_id
        else:
            raise exceptions.RunnerNotAvailable()

    def reset_runner(self):
        logger.debug('[Runner Heartbeat] - restarting runner')
        success = False

        for i in range(self.num_tries):
            try:
                success, _ = self.api_client.reset_runner()
            except Exception:
                logger.warning('[Runner Heartbeat] Runner is NOT available. Trial: {}/{}'.format(i, self.num_tries))
                success = False
            if success:
                break

        if not success:
            logger.critical('Failed to restart runner')

        return success

    @property
    def local_runner_id(self):
        return self.api_client.local_runner_id

    def handle_runner_reset_failure(self):
        # TODO - implement runner reset failure
        logger.critical('[Runner Heartbeat] RUNNER IS STUCK AND CANNOT BE REPAIRED. PLEASE STOP THE SERVICE MANUALLY!')

    def run(self):
        while True:
            try:
                runner_id = self.get_runner_id()
                if runner_id != self.local_runner_id:
                    logger.error(
                        '[Runner Heartbeat] Runner id has changed. Runner id: {}, previous id: {}'.format(
                            runner_id,
                            self.local_runner_id
                        )
                    )
                    self.api_client.set_runner_id(runner_id=runner_id)
                    self.api_client.handle_runner_reset()
                    raise exceptions.RunnerReset()
            except exceptions.RunnerNotAvailable:
                logger.exception('[Runner Heartbeat] Runner is not available')
                self.api_client.handle_runner_reset(force_all=True)
                success = self.reset_runner()
                if not success:
                    self.handle_runner_reset_failure()
                runner_id = self.api_client.wait_for_runner()
                logger.error('[Runner Heartbeat] Received new runner id: {}'.format(runner_id))
                self.api_client.set_runner_id(runner_id=runner_id)
            except exceptions.RunnerReset:
                logger.error(
                    '[Runner Heartbeat] Runner stopped unexpectedly. Nack was sent for all awaiting executions')
            except Exception:
                logger.exception('[Runner Heartbeat] Exception raised while getting runner id')

            time.sleep(self.heartbeat_time)
