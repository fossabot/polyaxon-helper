# -*- coding: utf-8 -*-
from __future__ import absolute_import, division, print_function

import json
import os

from datetime import datetime


def get_cluster_def():
    cluster = os.getenv('PLX_CLUSTER', None)
    return json.loads(cluster) if cluster else None


def get_declarations():
    declarations = os.getenv('PLX_DECLARATIONS', None)
    return json.loads(declarations) if declarations else None


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
