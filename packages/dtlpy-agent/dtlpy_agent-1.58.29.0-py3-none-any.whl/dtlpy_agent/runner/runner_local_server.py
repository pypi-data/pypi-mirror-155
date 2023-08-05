import tornado.concurrent
import tornado.escape
import tornado.ioloop
import tornado.web
import tornado.websocket
import tornado.gen
import logging
import tornado
import os
from tornado  import web

logger = logging.getLogger('AgentRunner.WebApp')


# noinspection PyAbstractClass
class RunnerWebsocket(tornado.websocket.WebSocketHandler):

    def on_message(self, message):
        if self.application.client_api.is_runner_available():
            args = tornado.escape.json_decode(message)
            self.application.client_api.run_in_executor(args=args)
            self.write_message('true')
        else:
            self.write_message('false')


# noinspection PyAbstractClass
class MainHandler(tornado.web.RequestHandler):
    def get(self):
        status = 200 if self.application.client_api.is_runner_available() else 202
        self.set_status(status)
        self.finish()

    def delete(self):
        try:
            logger.warning('Execution termination request was received from proxy')
            args = tornado.escape.json_decode(self.request.body)
            execution_id = args['execution_id']
            self.application.client_api.terminate_execution(execution_id=execution_id)
            self.set_status(200)
        except Exception:
            self.set_status(400)


# noinspection PyAbstractClass
class TerminationHandler(tornado.web.RequestHandler):
    def post(self):
        logger.critical('Termination signal received from proxy. Terminating..')
        self.set_status(200)
        self.finish()
        # noinspection PyProtectedMember
        os._exit(os.EX_OSERR)


# noinspection PyAbstractClass
class RunnerIdHandler(tornado.web.RequestHandler):

    def get(self):
        self.set_status(200)
        runner_id = self.application.client_api.get_runner_id()
        self.write({'runner_id': runner_id})
        self.finish()


class AppHandler(tornado.web.RequestHandler):

    def get(self):
        self.set_status(200)
        runner_id = self.application.client_api.get_runner_id()
        self.write({'runner_id': runner_id})
        self.finish()


def _get_handler(site_dir, StaticFileHandler):
    from tornado.template import Loader

    class WebHandler(StaticFileHandler):

        def write_error(self, status_code, **kwargs):

            if status_code in (404, 500):
                error_page = '{}.html'.format(status_code)
                if os.path.isfile(os.path.join(site_dir, error_page)):
                    self.write(Loader(site_dir).load(error_page).generate())
                else:
                    super().write_error(status_code, **kwargs)

    return WebHandler


class ExternalHttpServer(tornado.web.Application):
    def __init__(self, client_api):
        ui_path = client_api.package_path + '/ui'
        handlers = [(r"/serve/(.*)", _get_handler(ui_path, web.StaticFileHandler), {
                    "path": ui_path,
                    "default_filename": "index.html"
                })]
        settings = {'debug': True}
        super().__init__(handlers, **settings)
        self.client_api = client_api

    def run(self, port):
        self.listen(port=port, address='0.0.0.0')
        logger.info("Agent Runner is up and listening on port {}".format(port))
        tornado.ioloop.IOLoop.current().start()


class WebServer(tornado.web.Application):
    def __init__(self, client_api):
        handlers = [
            (r"/web-socket", RunnerWebsocket),
            (r"/", MainHandler),
            (r"/runner_id", RunnerIdHandler),
            (r"/termination", TerminationHandler)
        ]

        settings = {'debug': True}
        super().__init__(handlers, **settings)
        self.client_api = client_api

    def run(self, port):
        self.listen(port=port, address='127.0.0.1')
        logger.info("Agent Runner is up and listening on port {}".format(port))
        tornado.ioloop.IOLoop.current().start()
