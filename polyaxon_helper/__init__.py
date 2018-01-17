# -*- coding: utf-8 -*-
from __future__ import absolute_import, division, print_function

import json
import os

import requests
import six


def get_cluster_def():
    """Returns cluster definition created by polyaxon.

    {
        "master": ["plxjob-master0-8eefb7a1146f476ca66e3bee9b88c1de:2000"],
        "worker": ["plxjob-worker1-8eefb7a1146f476ca66e3bee9b88c1de:2000",
                   "plxjob-worker2-8eefb7a1146f476ca66e3bee9b88c1de:2000"],
        "ps": ["plxjob-master0-8eefb7a1146f476ca66e3bee9b88c1de:2000"],
    }

    :return: dict
    """
    cluster = os.getenv('POLYAXON_CLUSTER', None)
    return json.loads(cluster) if cluster else None


def get_declarations():
    """Returns all the experiment declarations based on both:

        * declarations section
        * matrix section
    """
    declarations = os.getenv('POLYAXON_DECLARATIONS', None)
    return json.loads(declarations) if declarations else None


def get_experiment_info():
    """Returns information about the experiment:
        * project_name
        * experiment_group_name
        * experiment_name
        * project_uuid
        * experiment_group_uuid
        * experiment_uuid
    """
    info = os.getenv('POLYAXON_EXPERIMENT_INFO', None)
    return json.loads(info) if info else None


def get_task_info():
    """Returns the task info: {"type": str, "index": int}."""
    info = os.getenv('POLYAXON_TASK_INFO', None)
    return json.loads(info) if info else None


def get_outputs_path():
    """The ouputs path generated by polyaxon based on the hierarchy of the experiment:

        `user/project/group/experiment/files`
    """
    return os.getenv('POLYAXON_OUTPUTS_PATH', None)


def get_data_path():
    """The data path generated by polyaxon based on the hierarchy of the projet:

        `user/project/`
    """
    return os.getenv('POLYAXON_DATA_PATH', None)


def get_tf_config(envvar='TF_CLUSTER'):
    """Returns the TF_CONFIG defining the cluster and the current task.

    if `envvar` is not null, it will set and env variable with `envvar`.
    """
    cluster_def = get_cluster_def()
    task_info = get_task_info()
    tf_config = {
        'cluster': cluster_def,
        'task': task_info,
        'model_dir': get_outputs_path(),
        'environment': 'cloud'
    }

    if envvar:
        os.environ[envvar] = tf_config

    return tf_config


def get_log_level():
    """If set on the polyaxonfile it will return the log level."""
    return os.getenv('POLYAXON_LOG_LEVEL', None)


def get_api(version='v1'):
    api = os.getenv('POLYAXON_API', None)
    return '{}/api/{}'.format(api, version)


def get_user_token():
    return os.getenv('POLYAXON_USER_TOKEN', None)


def send_metrics(**metrics):
    """Sends metrics to polyaxon api.

    Example:
        send_metric(precision=0.9, accuracy=0.89, loss=0.01)
    """
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
