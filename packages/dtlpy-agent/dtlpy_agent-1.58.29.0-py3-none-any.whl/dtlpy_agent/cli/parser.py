# TODO - Remove different ways of accepting arguments
import argparse


class PackageOperations:
    RUNNER = 'runner'
    PROXY = 'proxy'
    SINGLE = 'single'


def get_parser() -> argparse.ArgumentParser:
    """
    Build the parser for CLI
    :return: parser object
    """
    parser = argparse.ArgumentParser(
        description="CLI for Dataloop Agent",
        formatter_class=argparse.RawTextHelpFormatter
    )

    ###############
    # sub parsers #
    ###############
    subparsers = parser.add_subparsers(dest="operation", help="supported operations")

    #################
    # Remote Runner #
    #################
    runner_parser = subparsers.add_parser(PackageOperations.RUNNER, help="Login by passing a valid token")

    runner_args = runner_parser.add_argument_group("Named arguments")

    runner_args.add_argument(
        '--env',
        type=str,
        dest='env',
        help="Environment (local, dev, prod, rc)")

    runner_args.add_argument(
        '--service-id',
        type=str,
        dest='service_id',
        help="service ID")

    runner_args.add_argument(
        '--service_id',
        type=str,
        dest='service_id',
        help="service ID")

    runner_args.add_argument(
        '--project-id',
        type=str,
        dest='project_id',
        help="Project ID")

    runner_args.add_argument(
        '--project',
        type=str,
        dest='project_id',
        help="Project ID")

    runner_args.add_argument(
        '--package-rev',
        type=str,
        required=False,
        default=None,
        dest='package_rev',
        help="Package revision")

    runner_args.add_argument(
        '--package_rev',
        type=str,
        required=False,
        default=None,
        dest='package_rev',
        help="Package revision")

    ################
    # Remote Proxy #
    ################
    proxy_parser = subparsers.add_parser(PackageOperations.PROXY, help="Login by passing a valid token")

    proxy_args = proxy_parser.add_argument_group("Named arguments")

    proxy_args.add_argument(
        '--env',
        type=str,
        dest='env',
        help="Environment (local, dev, prod)")

    proxy_args.add_argument(
        '--username',
        type=str,
        dest='username',
        help="Pipeline username")

    proxy_args.add_argument(
        '--password',
        type=str,
        dest='password',
        help="Password for the specified username")

    proxy_args.add_argument(
        '--client-id',
        type=str,
        dest='client_id',
        help="Client application id of the auth0 app to log in to")

    proxy_args.add_argument(
        '--client-secret',
        type=str,
        dest='client_secret',
        help="Client secret")

    proxy_args.add_argument(
        '--service',
        type=str,
        dest='service_id',
        help="Specify service id")

    proxy_args.add_argument(
        '--service-id',
        type=str,
        dest='service_id',
        help="Specify service id")

    proxy_args.add_argument(
        '--mq-host',
        type=str,
        dest='mq_host',
        help="RabbitMQ host")

    proxy_args.add_argument(
        '--project',
        type=str,
        dest='project_id',
        help="Platform projects to run task from.")

    proxy_args.add_argument(
        '--project-id',
        type=str,
        dest='project_id',
        help="Platform projects to run task from.")

    proxy_args.add_argument(
        '--mq-user',
        type=str,
        dest='mq_user',
        required=False,
        help="RabbitMQ username")

    proxy_args.add_argument(
        '--mq-password',
        type=str,
        dest='mq_password',
        required=False,
        help="RabbitMQ password")

    proxy_args.add_argument(
        '--mq-queue',
        type=str,
        dest='mq_queue',
        required=False,
        default=None,
        help="RabbitMQ queue name")

    proxy_args.add_argument(
        '--mq-prefetch',
        type=int,
        dest='mq_prefetch',
        required=False,
        default=1,
        help="RabbitMQ prefetch count (number of messages to handle at the same time)")

    ################
    # Single Agent #
    ################
    single_agent_parser = subparsers.add_parser(PackageOperations.SINGLE, help="Login by passing a valid token")

    single_args = single_agent_parser.add_argument_group("Named arguments")

    single_args.add_argument(
        '--env',
        type=str,
        dest='env',
        help="Environment (local, dev, prod)")

    single_args.add_argument(
        '--username',
        type=str,
        dest='username',
        help="Pipeline username")

    single_args.add_argument(
        '--password',
        type=str,
        dest='password',
        help="Password for the specified username")

    single_args.add_argument(
        '--client-id',
        type=str,
        dest='client_id',
        help="Client application id of the auth0 app to log in to")

    single_args.add_argument(
        '--client-secret',
        type=str,
        dest='client_secret',
        help="Client secret")

    single_args.add_argument(
        '--service',
        type=str,
        dest='service_id',
        help="Specify service id")

    single_args.add_argument(
        '--service-id',
        type=str,
        dest='service_id',
        help="Specify service id")

    single_args.add_argument(
        '--mq-host',
        type=str,
        dest='mq_host',
        help="RabbitMQ host")

    single_args.add_argument(
        '--project',
        type=str,
        dest='project_id',
        help="Platform projects to run task from.")

    single_args.add_argument(
        '--project-id',
        type=str,
        dest='project_id',
        help="Platform projects to run task from.")

    single_args.add_argument(
        '--mq-user',
        type=str,
        dest='mq_user',
        required=False,
        help="RabbitMQ username")

    single_args.add_argument(
        '--mq-password',
        type=str,
        dest='mq_password',
        required=False,
        help="RabbitMQ password")

    single_args.add_argument(
        '--mq-queue',
        type=str,
        dest='mq_queue',
        required=False,
        default=None,
        help="RabbitMQ queue name")

    single_args.add_argument(
        '--mq-prefetch',
        type=int,
        dest='mq_prefetch',
        required=False,
        default=1,
        help="RabbitMQ prefetch count (number of messages to handle at the same time)")

    return parser
