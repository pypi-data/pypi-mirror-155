import os


def is_running_on_gke():
    """ Returns True if the binary is running inside a Kubernetes cluster."""
    return os.path.exists('/var/run/secrets/kubernetes.io')
