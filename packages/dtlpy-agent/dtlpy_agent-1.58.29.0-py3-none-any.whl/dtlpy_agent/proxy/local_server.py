import logging
from queue import Full

import dtlpy as dl
from prometheus_client.exposition import choose_encoder
from prometheus_client import REGISTRY
import tornado.ioloop
import tornado.escape
import tornado.web
import tornado.websocket
import tornado

from dtlpy_agent.proxy.ampq_connection_publisher import ExecutionStatusReport

logger = logging.getLogger(name='AgentProxy.WebServer')


class MainWebServer(tornado.web.Application):
    def __init__(self, api_client):
        handlers = [
            (r"/get_jwt", JwtHandler),
            (r"/execution_report", ExecutionReporterHandler),
            (r"/information_report", InformationReporterHandler),
            (r"/execution_status_update", ExecutionStatusUpdateHandler),
        ]

        settings = {'debug': True}
        super().__init__(handlers, **settings)
        # app globals
        self.api_client = api_client


class PrometheusWebServer(tornado.web.Application):
    def __init__(self, api_client):
        handlers = [(r"/metrics", MetricsHandler)]
        settings = {'debug': True}
        super().__init__(handlers, **settings)
        # globals
        self.api_client = api_client
        self.prometheus_metrics = self.api_client.prometheus_metrics


# noinspection PyAbstractClass
class InformationReporterHandler(tornado.web.RequestHandler):

    def post(self):
        args = tornado.escape.json_decode(self.request.body)
        self.application.api_client.send_information_report(_json=args)
        self.set_status(200)
        self.finish()

    def get(self):
        body = {
            'usage_interval': self.application.api_client.get_information_interval()
        }
        self.write(body)


# noinspection PyAbstractClass
class ExecutionReporterHandler(tornado.websocket.WebSocketHandler):

    def on_message(self, message):
        try:
            args = tornado.escape.json_decode(message)
            self.application.api_client.send_execution_report(_json=args.get('execution_report'))
            report = args.get('report', None)
            if report:
                self.application.api_client.push_to_report_queue(report=ExecutionStatusReport.from_json(_json=report))
            self.application.api_client.send_prometheus_metrics(_json=args.get('prometheus_metrics'))
        except Exception:
            logger.exception('Failed to handle execution report')


# noinspection PyAbstractClass
class ExecutionStatusUpdateHandler(tornado.websocket.WebSocketHandler):
    def on_message(self, message):
        try:
            args = tornado.escape.json_decode(message)
            report = ExecutionStatusReport.from_json(_json=args)
            self.application.api_client.push_to_report_queue(report=report)
        except Full:
            logger.exception(
                '[PiperReporting] - [{}] - Report queue is full - failed to push execution update report'.format(
                    self.__class__.__name__
                )
            )
        except Exception:
            logger.exception(
                '[PiperReporting] - [{}] Failed to handle execution update'.format(self.__class__.__name__))


# noinspection PyAbstractClass
class JwtHandler(tornado.web.RequestHandler):
    def get(self):
        if dl.token_expired():
            self.application.api_client.get_jwt()
        self.write({'jwt': dl.token()})


# noinspection PyAbstractClass
class MetricsHandler(tornado.web.RequestHandler):
    def post(self):
        args = tornado.escape.json_decode(self.request.body)
        self.application.api_client.handle_prometheus_update(args=args)

    def get(self):
        encoder, content_type = choose_encoder(self.request.headers.get('accept'))
        self.set_header("Content-Type", content_type)
        self.write(encoder(REGISTRY))
