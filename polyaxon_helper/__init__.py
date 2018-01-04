# -*- coding: utf-8 -*-
from __future__ import absolute_import, division, print_function

import json
import os

from datetime import datetime


def get_cluster_def():
    cluster = os.getenv('POLYAXON_CLUSTER', None)
    return json.loads(cluster) if cluster else None


def get_declarations():
    declarations = os.getenv('POLYAXON_DECLARATIONS', None)
    return json.loads(declarations) if declarations else None


def get_experiment_info():
    declarations = os.getenv('POLYAXON_INFO', None)
    return json.loads(declarations) if declarations else None


def send_metrics(**metrics):
    experiment_info = get_experiment_info()
    experiment_uuid = experiment_info.get('experiment_uuid', None)
    if not experiment_uuid:
        raise ValueError('`experiment_uuid` was not found.')

    try:
        from experiments.tasks import set_metrics

        set_metrics.delay(experiment_uuid=experiment_uuid,
                          created_at=datetime.utcnow(),
                          metrics=metrics)

    except ImportError:
        pass
