import io
import sys
import threading
import json
import logging


class AgentRedirect(io.StringIO):
    STDOUT = 'stdout'
    STDERR = 'stderr'

    def __init__(self, logger, std_type, *args, **kwargs):
        super(AgentRedirect, self).__init__(*args, **kwargs)
        self.logger = logger
        self.std_type = std_type

    def __enter__(self):
        return self

    def __exit__(self, *args):
        return False

    def write(self, s):

        if len(self.logger.handlers) > 1:
            self.logger.handlers = [h for h in self.logger.handlers if isinstance(h, AgentStreamHandler)]

        if self.std_type == self.STDOUT:
            self.logger.info(s)
        else:
            self.logger.error(s)

    def flush(self) -> None:
        pass


class AgentStreamHandler(logging.StreamHandler):

    def __init__(self, api_client):
        super(AgentStreamHandler, self).__init__(stream=sys.__stdout__)
        self.api_client = api_client

    @staticmethod
    def stringify_log_line(line: str, level: str, line_header: dict):
        output_dict = {
            'message': line,
            "level": level
        }
        output_dict.update(line_header)
        return '{}'.format(json.dumps(output_dict))

    @staticmethod
    def _get_thread_id():
        try:
            thread_id = threading.get_ident()
        except Exception:
            thread_id = 0
        return thread_id

    def _get_line_header(self, thread_id):
        line_header = {}
        if self.api_client is not None:
            try:
                line_header = self.api_client.get_header(thread_id)
            except Exception:
                pass

        return line_header

    def emit(self, record):
        try:
            thread_id = self._get_thread_id()
            line_header = self._get_line_header(thread_id=thread_id)

            if isinstance(record.msg, str) and record.msg.strip():
                msg = self.format(record)

                output_string = self.stringify_log_line(
                    line=msg,
                    level=record.levelname,
                    line_header=line_header
                )

                stream = self.stream
                # issue 35046: merged two stream.writes into one. - logging issue
                stream.write(output_string + self.terminator)
                self.flush()
        except RecursionError:  # See issue 36272 - logging issue
            raise
        except Exception:
            self.handleError(record)