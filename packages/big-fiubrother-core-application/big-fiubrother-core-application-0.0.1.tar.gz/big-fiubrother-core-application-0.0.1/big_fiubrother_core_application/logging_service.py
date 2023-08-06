import graypy
import logging
from logging.handlers import QueueListener, QueueHandler
from queue import Queue

DISTRIBUTED_KEY = 'distributed'


def create_distributed_logging_service(log_queue, application_name, configuration):
    graylog_handler = graypy.GELFUDPHandler(
        host=configuration['host'],
        port=configuration['port'],
        facility=application_name)

    return QueueListener(log_queue, graylog_handler)


class LoggingService:

    def __init__(self, application_name, configuration):
        self._initialize_logging()

        if DISTRIBUTED_KEY in configuration:
            self.distributed_logging_service = \
                create_distributed_logging_service(self.log_queue, application_name, configuration[DISTRIBUTED_KEY])

    def _initialize_logging(self):
        # logging.getLogger('pika').setLevel(logging.WARNING)
        # logging.getLogger('kazoo.client').setLevel(logging.INFO)

        self.log_queue = Queue()
        queue_handler = QueueHandler(self.log_queue)

        logging.basicConfig(level=logging.INFO,
                            handlers=[queue_handler])

        self.distributed_logging_service = None

    def start(self):
        if self.distributed_logging_service:
            self.distributed_logging_service.start()

    def stop(self):
        if self.distributed_logging_service:
            self.distributed_logging_service.stop()
