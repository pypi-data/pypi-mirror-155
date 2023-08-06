import ctypes
import pytest
import threading
import time
from typing import Type

from google.cloud import firestore


class Helpers:
    @staticmethod
    def recursive_delete(doc: firestore.DocumentReference):
        # uses ADC to get a privileged client (a service account with admin privileges)
        client = firestore.Client()
        doc = client.document(doc.path)
        for c in doc.collections():
            for d in c.stream():  # users/<user_id>/test_jobs/<job_id>/sequences/<seq_id>
                d.reference.delete()
        doc.delete()

    @staticmethod
    def patiently_wait_for_status(job_refs, expected_statuses):
        for _ in range(5):
            time.sleep(0.2)
            statuses = [job_ref.get().get('status') for job_ref in job_refs]

            if expected_statuses == statuses:
                return
        pytest.fail(f'Statuses {expected_statuses} never reached. Current statuses: {statuses}')

    @staticmethod
    def raise_exception_in_thread(t: threading.Thread, e: Type[BaseException]):
        """
        Send an exception to another thread. Useful for gracefully shutting down jobs running in an executor.
        Lifted from https://gist.github.com/liuw/2407154
        """
        ret = ctypes.pythonapi.PyThreadState_SetAsyncExc(ctypes.c_long(t.ident), ctypes.py_object(e))
        # ref: http://docs.python.org/c-api/init.html#PyThreadState_SetAsyncExc
        if ret == 0:
            raise ValueError("Invalid thread ID")
        elif ret > 1:
            # How could we possibly have notified more than one thread?
            # Because we punched a hole into C level interpreter.
            # So it is better to play safe and clean up the mess.
            ctypes.pythonapi.PyThreadState_SetAsyncExc(t.ident, None)
            raise SystemError("PyThreadState_SetAsyncExc failed")
