import requests
import logging
from urllib3.util import Retry
from requests.adapters import HTTPAdapter
import os

logger = logging.getLogger('AgentRunner.ApiClient.RequestSession')


class RequestSession:

    DEFAULT_POOL_MAX_SIZE = 10

    def __init__(self, retries=5, pool_maxsize=None):
        self.retries = retries
        self._session = None
        self._pool_maxsize = pool_maxsize

    @property
    def pool_maxsize(self):
        if self._pool_maxsize is None:
            self._pool_maxsize = int(os.environ.get('CONCURRENCY', self.DEFAULT_POOL_MAX_SIZE)) + 3
        return self._pool_maxsize

    @property
    def session(self):
        if self._session is None:
            self._session = requests.Session()
            retry = Retry(
                total=5,
                read=5,
                connect=5,
                backoff_factor=0.3,
                # use on any request type
                method_whitelist=False,
                raise_on_status=False
            )
            adapter = HTTPAdapter(max_retries=retry, pool_maxsize=self.pool_maxsize)
            self._session.mount('http://', adapter)
            self._session.mount('https://', adapter)
        return self._session

    def get(self, port, name="", timeout=None):
        if name != "":
            name = '/' + name
        url = 'http://localhost:{port}{name}'.format(port=port, name=name)
        for i in range(self.retries):
            try:
                return self.session.get(url=url,
                                        timeout=timeout)
            except requests.exceptions.ConnectionError:
                logger.exception("ConnectionError session closed url: {}".format(url))
        raise Exception("Request acceded max retries")

    def post(self, port, json=None, name="", timeout=None):
        if name != "":
            name = '/' + name
        url = 'http://localhost:{port}{name}'.format(port=port, name=name)
        for i in range(self.retries):
            try:
                return self.session.post(url=url,
                                         timeout=timeout, json=json)
            except requests.exceptions.ConnectionError:
                logger.exception("ConnectionError session closed url: {}".format(url))
        raise Exception("Request acceded max retries")

    def delete(self, port, json=None, name="", timeout=None):
        if name != "":
            name = '/' + name
        url = 'http://localhost:{port}{name}'.format(port=port, name=name)
        for i in range(self.retries):
            try:
                return self.session.delete(url=url,
                                           timeout=timeout, json=json)
            except requests.exceptions.ConnectionError:
                logger.exception("ConnectionError session closed url: {}".format(url))
        raise Exception("Request acceded max retries")
