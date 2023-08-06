import json

from python_qa.logging.logging import Logging
import logging


class BaseLogging:
    log_level = logging.NOTSET
    log_format = None

    def log(self, data):
        try:
            content = json.dumps(data.json(), indent=4, ensure_ascii=False)
        except ValueError:
            content = data.text
        if type(data.request.body) is str:
            body = json.dumps(json.loads(data.request.body), indent=4, ensure_ascii=False)
        else:
            body = "-"
        Logging.logger.log(
            self.log_level, self.log_format.format(data=data, body=body, content=content)
        )


class LoggingResponseInfo(BaseLogging):
    log_format = (
        "Request: {data.request.method} {data.url} "
        "headers {data.request.headers}\n"
        "{body}\n"
        "Response: {data.status_code}\n"
        "{content}"
    )
    log_level = logging.INFO

    def run(self, response, *args, **kwargs):
        self.log(response)
