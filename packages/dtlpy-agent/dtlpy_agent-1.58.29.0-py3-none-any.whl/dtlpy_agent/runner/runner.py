import site
import subprocess
import threading
import importlib
import importlib.util
import logging
import inspect
import shutil
import sys
import ssl
import os
import base64
import json
import dtlpy as dl
from .gitUtils import GitUtils

# noinspection PyProtectedMember
ssl._create_default_https_context = ssl._create_unverified_context

logger = logging.getLogger('AgentRunner')


class Runner:

    def __init__(self, api_client):
        self.api_client = api_client
        self.git_utils = GitUtils()
        cache_available = os.environ.get('IS_CACHE_AVAILABLE', 'false') == 'true'

        if cache_available:
            if os.environ.get('NO_REDIS', 'fasle') == 'true':
                dl.sdk_cache.use_cache = True
                cache_path = os.environ.get('DEFAULT_CACHE_PATH', False)
                _json = {
                    'type': dl.CacheType.DISKCACHE.value,
                    'level': 1,
                    'options': {
                    }
                }

                if cache_path:
                    _json['options']['cachePath'] = cache_path

                base64_bytes = base64.b64encode(json.dumps(_json).encode("ascii"))
                base64_string = base64_bytes.decode("ascii")
                os.environ['CACHE_CONFIG'] = base64_string
                dl.client_api.build_cache(base64_string)
            else:
                redis_host = os.environ.get('REDIS_HOST', '127.0.0.1')
                redis_port = os.environ.get('REDIS_PORT', '6379')
                redis_ttl = os.environ.get('REDIS_TTL', '1000')
                _json = {
                    'type': 'redis',
                    'ttl': int(redis_ttl),
                    'level': 1,
                    'options': {
                        'host': redis_host,
                        'port': int(redis_port)
                    },
                }
                base64_bytes = base64.b64encode(json.dumps(_json).encode("ascii"))
                base64_string = base64_bytes.decode("ascii")
                os.environ['CACHE_CONFIG'] = base64_string
                dl.client_api.build_cache(base64_string)

    @property
    def project(self) -> dl.entities.Project:
        return self.api_client.project

    @property
    def package(self) -> dl.entities.Package:
        return self.api_client.package

    @property
    def service(self) -> dl.entities.Service:
        return self.api_client.service

    @property
    def service_runtime(self) -> dl.entities.KubernetesRuntime:
        if isinstance(self.service.runtime, dict):
            runtime = dl.entities.KubernetesRuntime(**self.service.runtime)
        else:
            runtime = self.service.runtime
        return runtime

    @property
    def num_workers(self) -> int:
        return self.service_runtime.concurrency

    def _get_entities(self, project_id: str, service_id: str):
        if self.project is None:
            self.api_client.project = dl.projects.get(project_id=project_id)

        if self.service is None:
            self.api_client.service = dl.services.get(service_id=service_id)

        if self.package is None:
            self.api_client.package = dl.packages.get(package_id=self.service.package_id)

    def load_package(self, project_id: str, service_id: str):
        self.api_client.redirect_thread_logs(
            thread_id=threading.get_ident(),
            execution=None,
            function_name='init_service'
        )
        try:
            logger.info('[Start] {}'.format('Loading package'))
            logger.info('[Start] {}'.format('Getting package entities.'))

            # get package revision
            package_revision = self._get_package_revision()

            self.api_client.set_num_workers(self.num_workers)
            logger.info('Concurrency was set to {}.'.format(self.num_workers))

            # download codebase
            self._download_codebase(service_id=service_id, package_revision=package_revision)

            # add to path
            sys.path.append(os.getcwd())

            # add dtlpy instance input if needed
            if hasattr(self.service, 'use_user_jwt') and self.service.use_user_jwt:
                self.service.init_input['dl'] = dl

            # install requirements
            self._install_requirements()

            # try load the runner from filename
            faas_path = self.api_client.package_path
            if self.package.type == 'app':
                faas_path = faas_path + '/functions'
            service_runner = self._load_runner(package_path=faas_path)
            if service_runner is None:
                return
            if hasattr(service_runner, '_service_entity'):
                service_runner.service_entity = self.service

            # run init
            logger.info('[Start] {}'.format('Running ServiceRunner init.'))
            service_runner_object = service_runner(**self.service.init_input)
            logger.info('[Done] {}'.format('Running ServiceRunner init.'))

            self.api_client.set_service_runner(service_runner=service_runner_object)

            logger.info('[Done] {}'.format('Loading package'))
        except Exception:
            logger.exception('Failed to load runner')
            raise
        finally:
            self.api_client.undo_redirect_thread_logs(thread_id=threading.get_ident())

    def _get_package_path(self, service_id: str) -> str:
        package_revision = os.environ.get("PACKAGE_REVISION", '1.0.0')
        packages_path = os.path.join(os.path.expanduser('~'), 'packages')
        packages_path = os.path.abspath(packages_path)
        package_path = os.path.abspath(os.path.join(packages_path, service_id, package_revision))
        try:
            os.makedirs(package_path, exist_ok=True)
            os.chdir(package_path)
        except Exception:
            logger.exception('Unable to make dir: {}'.format(packages_path))
            raise
        return package_path

    def _download_codebase(self, service_id: str, package_revision: dl.entities.Package) -> str:
        if package_revision.codebase is not None \
                and package_revision.codebase.type not in [dl.PackageCodebaseType.FILESYSTEM,
                                                           dl.PackageCodebaseType.LOCAL]:
            logger.info('[Start] {}'.format('Downloading package codebase.'))
            package_path = self.api_client.package_path
            self._get_package_source_code(package_revision=package_revision, local_path=package_path)

            logger.info('Source Code was downloaded to {}.'.format(package_path))
            logger.info('[Done] {}'.format('Downloading package codebase.'))
            logger.info('[Start] {}'.format('Importing package runner from: {}'.format(package_path)))

            # check if zip was for root dir and enter it if yes
            dirs = os.listdir(os.getcwd())
            if len(dirs) == 1 and os.path.isdir(os.path.join(os.getcwd(), dirs[0])):
                os.chdir(os.path.join(os.getcwd(), dirs[0]))
        elif package_revision.codebase is not None \
                and package_revision.codebase.type in [dl.PackageCodebaseType.FILESYSTEM, dl.PackageCodebaseType.LOCAL]:
            logger.info('[Start] {}'.format('Changing cwd to codebase path.'))

            if package_revision.codebase.type == dl.PackageCodebaseType.FILESYSTEM:
                package_path = package_revision.codebase.container_path
            else:
                package_path = package_revision.codebase.local_path

            try:
                os.chdir(package_path)
                logger.info('[Start] {}'.format('Changing cwd to codebase path.'))
            except Exception:
                logger.exception('Unable to change working directory to: {}'.format(package_path))
                raise
        else:
            raise Exception('Package has no codebase')

        return package_path

    def _load_runner(self, package_path):
        if hasattr(self.service, 'module_name') and hasattr(self.package, 'modules'):
            module = [m for m in self.package.modules if m.name == self.service.module_name]
            if len(module) != 1 and self.package.type == 'app':
                return
            if len(module) != 1:
                logger.warning('Cant get entry point. trying to get main.py ')
                entry_point = 'main.py'
                class_name = 'ServiceRunner'
            else:
                module = module[0]
                entry_point = module.entry_point
                class_name = getattr(module, 'class_name', 'ServiceRunner')
        else:
            entry_point = 'main.py'
            class_name = 'ServiceRunner'

        logger.info('[Start] {}'.format('Loading class and module from file'))
        logger.info('Importing package runner from: '.format(package_path))
        logger.info('Entry point found: ' + entry_point)
        logger.info('Class name found: ' + class_name)

        sys.path.append(site.USER_SITE)

        spec = importlib.util.spec_from_file_location(class_name, entry_point)
        # load class from file
        module_from_spec = importlib.util.module_from_spec(spec)
        spec.loader.exec_module(module_from_spec)
        service_runner = getattr(module_from_spec, class_name)
        logger.info('[Done] {}'.format('Loading class and module from file'))

        return service_runner

    def _install_requirements(self):
        if self.package.requirements is None or len(self.package.requirements) == 0:
            requirements_path = os.path.join(os.getcwd(), 'package_requirements.txt')
            if not os.path.isfile(requirements_path):
                requirements_path = os.path.join(os.getcwd(), 'requirements.txt')
            if os.path.isfile(requirements_path):
                logger.info('[Start] {}'.format('Installing requirements'))
                success = self._install_from_file(requirements_path=requirements_path)
                if success:
                    logger.info('[Done] {}'.format('Installing requirements'))
                else:
                    raise Exception('[Failed] {}'.format('Installing requirements'))

    @staticmethod
    def _bytes_to_string(output):
        if isinstance(output, bytes):
            output = output.decode("utf-8")

        return output

    def _install_from_file(self, requirements_path):
        if shutil.which('pip3') is not None:
            pip_cmd = 'pip3'
        elif shutil.which('pip') is not None:
            pip_cmd = 'pip'
        else:
            raise ValueError('missing "pip3" and "pip". failed installing requirements')
        logger.info('Found {} installation. Location: {!r}'.format(pip_cmd, shutil.which(pip_cmd)))

        p = subprocess.Popen([pip_cmd, 'install', '-r', requirements_path, '--user'],
                             stdout=subprocess.PIPE,
                             stderr=subprocess.PIPE)

        out, err = p.communicate()
        success = p.returncode == 0

        if not success:
            logger.error(self._bytes_to_string(output=err))
        else:
            logger.debug(self._bytes_to_string(output=out))

        if success:
            try:
                for key in globals():
                    if inspect.ismodule(globals()[key]):
                        importlib.reload(globals()[key])
            except Exception:
                logger.exception('Failed to reload modules')
                success = False

        return success

    def _get_package_revision(self) -> dl.entities.Package:
        package_revision = self.service.package_revision

        if self.package.version == package_revision:
            return self.package

        for rev in self.package.revisions:
            if rev['version'] == package_revision:
                # noinspection PyProtectedMember
                return dl.entities.Package.from_json(
                    _json=rev,
                    client_api=self.package._client_api,
                    project=self.package._project
                )

        raise Exception('Package {} does not include revision: {}'.format(self.package.name, package_revision))

    def _get_single(self, codebase: dl.GitCodebase, name: str):
        value = None
        integration_id = codebase.credentials.get(name, {}).get('id', None)
        key = codebase.credentials.get(name, {}).get('key', None)

        if integration_id is not None:
            try:
                key = self.project.integrations.get(integrations_id=integration_id).name
            except Exception:
                pass
            value = os.environ.get(key, None)

        return value

    def _get_credential(self, codebase: dl.GitCodebase):
        username = password = None

        if codebase.credentials:
            try:
                username = self._get_single(codebase=codebase, name='username')
                password = self._get_single(codebase=codebase, name='password')
            except Exception:
                logger.exception('Failed to get credentials from codebase')

        return username, password

    def _get_package_source_code(self, package_revision: dl.entities.Package, local_path: str):
        if package_revision.codebase is None or package_revision.codebase.type == dl.PackageCodebaseType.ITEM:
            package_revision.pull(
                version=self.service.package_revision,
                local_path=local_path
            )
        elif package_revision.codebase.type == dl.PackageCodebaseType.GIT:
            username, password = self._get_credential(codebase=package_revision.codebase)
            self.git_utils.git_clone(
                local_path=local_path,
                git_url=package_revision.codebase.git_url,
                tag=package_revision.codebase.git_tag,
                username=username,
                password=password
            )
        else:
            raise Exception('[RUNNER] Unknown codebase type: {}'.format(package_revision.codebase.type))

    def start(self, project_id: str, service_id: str):
        self.api_client.package_path = self._get_package_path(service_id)
        runner_server = self.api_client.start_local_server()
        self.api_client.wait_for_proxy()
        self.api_client.init_runner_ws_client()
        self.api_client.start_runner_monitoring()
        self._get_entities(project_id=project_id, service_id=service_id)

        dl.client_api.default_headers = {"x-dl-endpoint-id": service_id}
        logger.info('Setting request headers: {}'.format(dl.client_api.default_headers))
        try:
            self.load_package(project_id=project_id, service_id=service_id)
        except Exception:
            self.api_client.set_monitoring_status(status='failed')
            raise

        logger.info('Package was loaded successfully:')
        logger.info('Package name: {}'.format(self.package.name))
        logger.info('Package revision: {}'.format(self.service.package_revision))
        logger.info('Service name: {}'.format(self.service.name))
        logger.info('Runtime params: {}'.format(self.service_runtime.to_json()))

        #########################
        # Start main web server #
        #########################
        self.api_client.set_monitoring_status(status='running')
        self.api_client.runner_started()
        logger.info('RUNNER IS UP :)')
        runner_server.join()
