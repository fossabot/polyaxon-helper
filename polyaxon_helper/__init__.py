# -*- coding: utf-8 -*-
from __future__ import absolute_import, division, print_function

import json
import os

import requests
import six


def get_cluster_def():
    cluster = os.getenv('POLYAXON_CLUSTER', None)
    return json.loads(cluster) if cluster else None


def get_log_level():
    cluster = os.getenv('POLYAXON_LOG_LEVEL', None)
    return json.loads(cluster) if cluster else None


def get_outputs_path():
    return os.getenv('POLYAXON_OUTPUTS_PATH', None)


def get_declarations():
    declarations = os.getenv('POLYAXON_DECLARATIONS', None)
    return json.loads(declarations) if declarations else None


def get_experiment_info():
    declarations = os.getenv('POLYAXON_EXPERIMENT_INFO', None)
    return json.loads(declarations) if declarations else None


def get_api(version='v1'):
    api = os.getenv('POLYAXON_API', None)
    return '{}/api/{}'.format(api, version)


def get_user_token():
    return os.getenv('POLYAXON_USER_TOKEN', None)


def send_metrics(**metrics):
    experiment_info = get_experiment_info()
    experiment_name = experiment_info.get('experiment_name', None)
    user_token = get_user_token()
    api = get_api()
    if not all([experiment_name, user_token, api]):
        print('Environment information not found, '
              'please make sure this is running inside a polyaxon job.')
        return

    values = experiment_name.split('.')
    user, project, experiment = values[0], values[1], values[-1]

    try:
        formatted_metrics = {k: float(v) for k, v in six.iteritems(metrics)}
    except (ValueError, TypeError):
        print('could not send metrics {}'.format(metrics))
        return

    try:
        requests.post('{}/{}/{}/experiments/{}/metrics'.format(api, user, project, experiment),
                      headers={"Authorization": "token {}".format(user_token)},
                      data={'values': json.dumps(formatted_metrics)})
    except requests.RequestException as e:
        print('could not reach polyaxon api {}'.format(e))
