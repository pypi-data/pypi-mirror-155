import os
import time


def is_running_on_gke():
    """ Returns True if the binary is running inside a Kubernetes cluster."""
    return os.path.exists('/var/run/secrets/kubernetes.io')


def current_time_ms():
    """ Returns the current time in milliseconds since EPOCH """
    return time.time_ns() // 1_000_000
