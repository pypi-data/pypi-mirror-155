import os
import dtlpy as dl
from dtlpy_agent.cli.executor import run_agent
from dtlpy_agent.cli.parser import PackageOperations

env = 'dev'
service_id = '6256d1d1cda7684adb995870'
operation = PackageOperations.RUNNER

# dl.login()


class Args:
    def __init__(self, **kwargs):
        for key, val in kwargs.items():
            setattr(self, key, val)


dl.setenv(env=env)
service = dl.services.get(service_id=service_id)

args = Args(
    env=env,
    operation=operation,
    username='pipelines@dataloop.ai',
    password=os.environ.get('BOT_PASSWORD_{}'.format(env.upper())),
    client_id=os.environ.get('CLIENT_ID_{}'.format(env.upper())),
    client_secret=os.environ.get('CLIENT_SECRET_{}'.format(env.upper())),
    project_id=service.project_id,
    service_id=service_id,
    mq_queue='{}-{}'.format(service.name, service.id),
    mq_host=os.environ.get('MQ_HOST_{}'.format(env.upper())),
    mq_user=os.environ.get('MQ_USER_{}'.format(env.upper())),
    mq_password=os.environ.get('MQ_PASSWORD_{}'.format(env.upper())),
    mq_prefetch=service.runtime.concurrency
)

# noinspection PyUnresolvedReferences
runner_command = "agnt runner --env {env} --usernaem pipelines@dataloop.ai --password {password} " \
                 "--client-id {client_id} --client-secret {client_secret} --service_id {service_id} " \
                 "--mq-host {mq_host} --project {project_id} --mq-user {mq_user} --mq-password {mq_password} " \
                 "--mq-queue {queue} --mq-prefetch {prefetch}".format(env=env,
                                                                      password=args.password,
                                                                      client_id=args.client_id,
                                                                      client_secret=args.client_secret,
                                                                      service_id=service_id,
                                                                      mq_host=args.mq_host,
                                                                      project_id=service.project_id,
                                                                      mq_user=args.mq_user,
                                                                      mq_password=args.mq_password,
                                                                      prefetch=service.runtime.concurrency,
                                                                      queue=args.mq_queue
                                                                      )
print(runner_command)


run_agent(args=args)
