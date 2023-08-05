import dtlpy as dl
import traceback
import logging
import ssl
import sys

from .. import exceptions

# noinspection PyProtectedMember
ssl._create_default_https_context = ssl._create_unverified_context

logging.basicConfig(level=logging.DEBUG,
                    format='%(asctime)s - %(name)s - %(levelname)s - %(thread)d - %(message)s')
logger = logging.getLogger(name='AgentProxy')
logging.getLogger('urllib3').setLevel(logging.WARN)
logging.getLogger('tornado').setLevel(logging.WARN)
logging.getLogger('amqpstorm').setLevel(logging.WARN)

stdout_handler = logging.StreamHandler(sys.stdout)
stdout_handler.setLevel(logging.DEBUG)


class Proxy:
    def __init__(self, api_client):
        self.api_client = api_client

    def start(self):
        while True:
            try:
                self.api_client.set_monitoring_status(status='running')
            except Exception:
                logger.exception('Failed to set monitoring status')

            try:
                logger.info('PROXY IS UP :)')
                self.api_client.start_consuming(on_message=self.on_message)
            except Exception:
                logger.exception('[MQ CONNECTION ERROR] Exception raised!')
                logger.info('[MQ CONNECTION] Reconnecting to mq!')

    @staticmethod
    def _get_event_params(message: dict):
        resource = None
        action = None
        resource_type = None
        context = None
        user_token = message.pop('jwt', None)
        event_context = message.pop('eventContext', dict())

        try:
            event = message.pop('event', None)

            if event:
                resource = event.get('body', None)
                context = event.get('context', None)

                event = event.get('event', dict())

                action = event.get('action', None)
                resource_type = event.get('resource', None)
        except Exception:
            logger.warning('Failed to get event params')

        return resource_type, action, resource, context, user_token, event_context

    def on_message(self, execution: dict, delivery_tag: str):
        try:
            resource_type, action, resource, context, user_token, event_context = self._get_event_params(
                message=execution
            )

            logger.info('[Start] Execution created: {}'.format(execution))

            try:
                execution_inputs = self.get_execution_input(
                    execution=execution,
                    package=self.api_client.package,
                    service=self.api_client.service
                )

                message_to_send = {
                    'execution_inputs': execution_inputs,
                    'execution': execution,
                    'user_token': user_token,
                    'resource_type': resource_type,
                    'action': action,
                    'resource': resource,
                    'context': context,
                    'event_context': event_context
                }

            except exceptions.MissingModule:
                if execution is not None:
                    self.api_client.send_execution_update_to_proxy(
                        execution_id=execution['id'],
                        status='failed',
                        percent_complete=0,
                        message=traceback.format_exc(),
                        output=[]
                    )
                raise
            except exceptions.MissingFunction:
                if execution is not None:
                    self.api_client.send_execution_update_to_proxy(
                        execution_id=execution['id'],
                        status='failed',
                        percent_complete=0,
                        message=traceback.format_exc(),
                        output=[]
                    )
                raise
            except Exception:
                logger.exception('[Failed] Getting execution input')
                raise exceptions.ParsingInputsError

            self.api_client.append_execution(
                execution=execution,
                delivery_tag=delivery_tag
            )

            success = self.api_client.send_execution_to_runner(payload=message_to_send)

            if not success:
                raise exceptions.RunnerNotAvailable()

        except exceptions.RunnerNotAvailable:
            self.pop_from_proxy_executions(execution=execution)
            logger.exception('[Failed] Check agent runner for availability (get request)')
            success = False
        except exceptions.ParsingInputsError:
            logger.exception('[Failed] Getting execution input...')
            success = False
        except exceptions.RunnerReset:
            self.pop_from_proxy_executions(execution=execution)
            logger.exception('[Failed] Runner reset while running execution')
            success = False
        except exceptions.MissingModule as e:
            logger.exception(e)
            success = True
        except exceptions.MissingFunction as e:
            logger.exception(e)
            success = True
        except Exception:
            self.pop_from_proxy_executions(execution=execution)
            logger.exception('[Failed] Unknown error occurred')
            success = False

        return success

    def pop_from_proxy_executions(self, execution: dict):
        if execution and 'id' in execution:
            self.api_client.pop_from_proxy_execution(execution_id=execution['id'])

    @staticmethod
    def get_execution_input(
            execution: dict,
            package: dl.entities.Package,
            service: dl.entities.Service
    ):
        module = [m for m in package.modules if m.name == service.module_name]
        module = module[0]
        func = [f for f in module.functions if f.name == execution['functionName']]
        func = func[0]
        expected_inputs = func.inputs
        execution_inputs = list()
        for input_field in expected_inputs:
            input_name = input_field.name
            if input_name in execution['input']:
                resource = input_field.type
                value = execution['input'][input_name]
                execution_inputs.append({
                    'type': resource,
                    'value': value,
                    'name': input_name
                })

        return execution_inputs
