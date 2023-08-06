import json
import logging
import threading
from unittest import mock

import pytest


class MockBlpop:
    def __init__(self, job_path: str, queue_name: str):
        """ Set up the mock redis queue to return a job ready to be folded as soon as start is released. """

        self.start = threading.Event()
        self.stop = threading.Event()
        self.called = threading.Event()
        self.called_again = threading.Event()
        self.iter = self.fake_iter()
        self.job_path = job_path
        self.queue_name = queue_name

    def fake_iter(self):
        self.called.set()
        self.start.wait()
        yield (self.queue_name, json.dumps({'path': self.job_path}))
        self.called_again.set()
        logging.info('Fake queue is now blocking...')
        self.stop.wait()

    def blpop(self, name: str):
        assert name == self.queue_name
        return next(self.iter)


class WaitableMock(mock.MagicMock):
    """
    Simple extension to MagicMock that allows waiting on a method to be called with specific parameters.
    Useful for testing multi-threaded apps.
    """

    def __init__(self, *args, **kwargs):
        super(WaitableMock, self).__init__(*args, **kwargs)
        self.event_class = kwargs.pop('event_class', threading.Event)
        self.event = self.event_class()
        self.expected_calls = {}
        self.actual_calls = []

    def _mock_call(self, *args, **kwargs):
        ret_value = super(WaitableMock, self)._mock_call(*args, **kwargs)

        for call in self._mock_mock_calls:
            event = self.expected_calls.get(call.args)
            if event and not event.is_set():
                event.set()

        self.actual_calls.append({'args', args, 'kwargs', kwargs})
        # Always set per mock event object to ensure the function is called for wait_until_called.
        self.event.set()

        return ret_value

    def wait_until_called(self, timeout=1):
        return self.event.wait(timeout=timeout)

    def wait_until_called_with(self, *args, timeout=1):
        # If there are args create a per argument list event object and if not wait for per mock event object.
        if args:
            if args not in self.expected_calls:
                event = self.event_class()
                self.expected_calls[args] = event
            else:
                event = self.expected_calls[args]
        else:
            event = self.event

        event.wait(timeout=timeout)
        if not event.is_set():
            pytest.fail(f'Expected call with \n{args}, but received only \n{self.actual_calls}')
        return event.is_set()
