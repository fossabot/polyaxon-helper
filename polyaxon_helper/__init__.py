import os

from datetime import datetime


def get_cluster_def():
    return os.getenv('PLX_CLUSTER', None)


def get_declarations():
    declaration_keys = os.getenv('PLX_DECLARATIONS', [])
    return {key: os.getenv(key, None) for key in declaration_keys}


def send_metrics(**metrics):
    experiment_uuid = os.getenv('experiment_uuid', None)
    if not experiment_uuid:
        raise ValueError('`experiment_uuid` was not found.')

    try:
        from experiments.tasks import set_metrics

        set_metrics.delay(experiment_uuid=experiment_uuid,
                          created_at=datetime.utcnow(),
                          metrics=metrics)

    except ImportError:
        pass

