from contextlib import contextmanager
from threading import Event
from setproctitle import setproctitle

from .application_arguments import parse_arguments
from .configuration import load_configuration
from .environment import load_environment
from .logging_service import LoggingService
from .runtime_context import RuntimeContext
from .signal_handler import SignalHandler


@contextmanager
def run(name):
    # Parse arguments of the application
    arguments = parse_arguments(name)

    # Load environment and configuration
    environment = load_environment(arguments)
    configuration = load_configuration(environment)

    # Set application name
    setproctitle(name)

    # Enable signal handling
    signal_handler = SignalHandler()

    # Start logging
    logging_service = LoggingService(name, configuration['logging'])
    logging_service.start()

    application = Application(name, environment, configuration)
    signal_handler.subscribe(application.stop)

    yield application

    # Stop logging
    logging_service.stop()


class Application:

    def __init__(self, name, environment, configuration):
        self.name = name
        self.runtime_context = RuntimeContext(environment, configuration)
        self._stop_event = Event()

    def is_stopped(self):
        return self._stop_event.is_set()

    def stop(self):
        self._stop_event.set()

    def wait(self):
        self._stop_event.wait()
