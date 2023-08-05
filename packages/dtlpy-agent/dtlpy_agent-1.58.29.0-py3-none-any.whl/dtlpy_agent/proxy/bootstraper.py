import logging
import dtlpy as dl
from .ampq_connection import Consumer
import redis

logger = logging.getLogger(name="AgentProxy.bootstraper")


# noinspection PyAttributeOutsideInit
class Bootstraper:
    def __init__(self,
                 username: str,
                 password: str,
                 client_id: str,
                 client_secret: str,
                 env: str,
                 mq_host: str,
                 mq_user: str,
                 mq_password: str,
                 mq_queue: str,
                 mq_prefetch: str,
                 project_id: str,
                 service_id: str):

        self.username = username
        self.password = password
        self.client_id = client_id
        self.client_secret = client_secret
        self.env = env
        self.mq_host = mq_host
        self.mq_user = mq_user
        self.mq_password = mq_password
        self.mq_queue = mq_queue
        self.mq_prefetch = mq_prefetch
        self.project_id = project_id
        self.service_id = service_id

    def setup(self):
        self.login()
        self.service = dl.services.get(service_id=self.service_id)
        self.package = dl.packages.get(package_id=self.service.package_id)
        self.project = dl.projects.get(project_id=self.project_id)

    @staticmethod
    def print_args(parsed_args):
        dont_print_list = ['password', 'secret']
        to_print_dict = dict()
        for key, val in parsed_args.__dict__.items():
            print_ok = True
            for dis in dont_print_list:
                if key.lower().find(dis.lower()) != -1:
                    print_ok = False
            if print_ok:
                to_print_dict[key] = val
            else:
                to_print_dict[key] = '*****'
        logger.debug('args: {}'.format(to_print_dict))

    def get_token_from_redis(self, redis_cache):
        key_cache = self.service_id + '-' + self.username
        value_cache = redis_cache.get(key_cache)
        if value_cache:
            logger.info(msg='find in cache')
            dl.login_token(value_cache.decode('utf-8'))
            if dl.token_expired():
                logger.info(msg='token expired')
                return False
            logger.info(msg='login with redis')
            return True
        logger.info(msg='did not find in cache')
        return False

    def login(self):
        dl.setenv(self.env)
        redis_cache = None
        renewed = False

        if dl.client_api.refresh_token is not None:
            renewed = dl.client_api.renew_token()
        
        if not renewed:
            if self.env == 'dev':
                try:
                    redis_cache = redis.Redis(host='faas-cache', port=6379)
                    renewed = self.get_token_from_redis(redis_cache=redis_cache)
                except Exception:
                    redis_cache = None
                    logger.info('No Redis available')

            if not renewed:
                dl.login_m2m(
                    email=self.username,
                    password=self.password,
                    client_id=self.client_id,
                    client_secret=self.client_secret
                )
                if redis_cache and self.env == 'dev':
                    redis_cache.set(str(self.service_id + '-' + self.username), dl.token())

            # set client id to env - for refresh token
            dl.client_api.environments[dl.environment()]['client_id'] = self.client_id

    def get_ampq_mq_connection(self, on_message, on_failure):
        if isinstance(self.service.runtime, dict):
            self.mq_prefetch = self.service.runtime.get('concurrency', self.mq_prefetch)
        else:
            self.mq_prefetch = self.service.runtime.concurrency

        hostname, virtualhost = self.mq_host.split('/')

        return Consumer(
            hostname=hostname,
            username=self.mq_user,
            password=self.mq_password,
            queue=self.mq_queue or self.service.mq['queue'],
            number_of_consumers=self.mq_prefetch,
            on_message=on_message,
            virtual_host=virtualhost,
            env=self.env,
            max_attempts=self.service.max_attempts,
            on_failure=on_failure
        )
