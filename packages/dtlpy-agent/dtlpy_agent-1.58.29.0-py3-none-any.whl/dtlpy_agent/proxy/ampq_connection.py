import json
import logging
import threading
import time
import amqpstorm
from amqpstorm import Connection

logger = logging.getLogger(name='AgentProxy.mq_connection.consumer')


class Consumer(object):
    def __init__(self,
                 hostname: str,
                 username: str,
                 password: str,
                 queue: str,
                 max_attempts: int,
                 number_of_consumers: int,
                 on_message,
                 on_failure,
                 virtual_host='/',
                 env=None
                 ):

        self.hostname = hostname
        self.username = username
        self.password = password
        self.queue = queue
        self.prefetch = number_of_consumers
        self.max_retries = 5
        self._connection = None
        self._consumer = None
        self._stopped = threading.Event()
        self.on_message = on_message
        self.on_failure = on_failure
        self.virtual_host = virtual_host
        self.env = env
        self.channel = None
        self._pause = False
        self._max_attempts = max_attempts

    def start(self):
        """
        Start the Consumers.
        """
        self._stopped.clear()
        if not self._connection or self._connection.is_closed:
            self._create_connection()

        while not self._stopped.is_set():
            self.channel = None
            try:
                self.channel = self._connection.channel(rpc_timeout=10)
                self.channel.basic.qos(self.prefetch)
                self.channel.basic.consume(callback=self, queue=self.queue)
                self.channel.start_consuming()
                if not self.channel.consumer_tags:
                    # Only close the channel if there is nothing consuming.
                    # This is to allow messages that are still being processed
                    # in __call__ to finish processing.
                    self.channel.close()
            except amqpstorm.AMQPError as why:
                logger.exception(why)
                self._create_connection()
            finally:
                time.sleep(1)

    def stop(self):
        """
        Stop all consumers.
        """
        self._consumer.stop()
        self._stopped.set()
        self._connection.close()

    def ack(self, delivery_tag: str):
        self.channel.basic.ack(delivery_tag=delivery_tag)

    def nack(self, delivery_tag: str):
        self.channel.basic.nack(delivery_tag=delivery_tag)

    @property
    def get_mq_connection_credentials(self) -> dict:
        if self.env is not None and self.env in ['local', 'minikube_local_mac']:
            return dict(
                hostname=self.hostname.split('/')[0],
                port=5672,
                username='guest',
                password='guest',
                virtual_host='dev',
                ssl=False
            )
        else:
            return dict(
                hostname=self.hostname,
                username=self.username,
                password=self.password,
                virtual_host=self.virtual_host
            )

    def _create_connection(self):
        """
        Create a connection.
        """
        attempts = 0
        while True:
            attempts += 1
            if self._stopped.is_set():
                break
            try:
                self._connection = Connection(**self.get_mq_connection_credentials)
                break
            except amqpstorm.AMQPError as why:
                logger.warning(why)
                if self.max_retries and attempts > self.max_retries:
                    raise Exception('max number of retries reached')
                time.sleep(min(attempts * 2, 30))
            except KeyboardInterrupt:
                break

    def pause(self):
        """
        Pause consumer.
        """
        self._pause = True

    def validate_attempts(self, message, execution):
        attempt = message.properties.get('headers', dict()).get('x-delivery-count', None)
        success = attempt is None or attempt < self._max_attempts

        if not success:
            self.on_failure(
                execution_id=execution['id'],
                status='failed',
                message='Execution has reached max attempts',
                timestamp=time.time() * 1000
            )

        return success

    def __call__(self, message):
        msg_body = message.body
        msg_channel = message.channel
        msg_method = message.method

        if self._pause:
            msg_channel.basic.nack(msg_method['delivery_tag'])
            self.stop()
        else:
            execution = json.loads(msg_body)

            if self.validate_attempts(message=message, execution=execution):
                success = self.on_message(execution, msg_method['delivery_tag'])
            else:
                success = False

            if not success:
                msg_channel.basic.nack(msg_method['delivery_tag'])
