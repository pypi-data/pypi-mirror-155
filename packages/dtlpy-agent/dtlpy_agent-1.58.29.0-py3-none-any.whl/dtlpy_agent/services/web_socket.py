from websocket import create_connection, WebSocket
from typing import Union
import logging
import json
import time

logger = logging.getLogger('Agent.Websocket')


class WebSocketClient:

    def __init__(
            self,
            url: str,
            timeout: int = 5,
            enable_multithread: bool = True,
            retries: int = 5,
            interval: int = 1
    ):
        self._ws = None
        self._url = url
        self._timeout = timeout
        self._enable_multithread = enable_multithread
        self._retries = retries
        self._interval = interval

    def init(self):
        self._ws = create_connection(
            url=self._url,
            timeout=self._timeout,
            enable_multithread=self._enable_multithread
        )
        logger.info('Successfully connected to websocket: {}'.format(self._url))

    @property
    def ws(self) -> WebSocket:
        if self._ws is None:
            self.init()
        return self._ws

    def reconnect(self):
        self.ws.connect(
            url=self._url,
            timeout=self._timeout,
            enable_multithread=self._enable_multithread
        )
        logger.info('Successfully connected to websocket: {}'.format(self._url))

    def send(self, message: Union[str, dict]):
        if isinstance(message, dict):
            message = json.dumps(message).encode('utf-8')

        for i in range(self._retries):
            try:
                return self.ws.send(message)
            except Exception:
                logger.exception(
                    'Failed to send message in websocket to: {}. Try: {}/{}'.format(self._url, i, self._retries)
                )
                time.sleep(self._interval)
                self.reconnect()

        raise Exception('Failed to renew websocket connection')

    def recv(self):
        for i in range(self._retries):
            try:
                return self.ws.recv()
            except Exception:
                logger.exception(
                    'Failed to recv message from websocket: {}. Try: {}/{}'.format(self._url, i, self._retries)
                )
                time.sleep(self._interval)
                self.reconnect()

        raise Exception('Failed to renew websocket connection')
