import logging
import sys
import traceback
import uuid

import yaml
from scrapy import Request


def configure_logging():
    logging.basicConfig(stream=sys.stdout, level=logging.INFO)


class AnalytixException(Exception):
    """
    An exception class which codifies and streamlines exception handling so that
    common exceptions can be displayed to the user more uniformly.

    For different error log levels which are classified, a stream will be executed
    to the default notification method.
    """

    def __init__(self, error_code: str, exception=None,
                 language_code: str = "en"):
        Exception.__init__(self)

        if exception:
            self.with_traceback(exception.__traceback__)

        with open('./errors.yaml', "r") as stream:
            try:
                error_messages = yaml.safe_load(stream=stream)
                if error_code not in error_messages['errors']:
                    raise ValueError('The exception class provided does not exist.')
                error = error_messages['errors'][error_code]
                self.error_code = error_code
                self.description = error['description']
                self.resolution = error['resolution']
                self.reference = error['reference']

                if error['uuid']:
                    self.error_id = uuid.uuid4()
                else:
                    self.error_id = None

                self.traceback = error['traceback']

                match error['logLevel']:
                    case "CRITICAL":
                        self.log_level = logging.CRITICAL
                    case "ERROR":
                        self.log_level = logging.ERROR
                    case "WARNING":
                        self.log_level = logging.WARNING
                    case "INFO":
                        self.log_level = logging.INFO
                    case _:
                        raise ValueError('The logging level provided is invalid.')
             

            except yaml.YAMLError as exc:
                print(exc)

    def log(self):
        logger = logging.getLogger("Exception")
        logger.setLevel(self.log_level)
        log_msg = "Error Code: {}, Error ID: {}".format(self.error_code, self.error_id)
        if self.traceback:
            tracebacks = traceback.format_exception(AnalytixException, self, self.__traceback__)
            log_msg += "\n" + ''.join(tracebacks)
        logger.log(self.log_level, log_msg)

        # TODO: Need to route this to some notification service.
        # if self.log_level == 'Critical':
        #     yield Request()
