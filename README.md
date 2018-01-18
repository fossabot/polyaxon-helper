<!-- [![Build Status](https://travis-ci.org/polyaxon/polyaxon-helper.svg?branch=master)](https://travis-ci.org/polyaxon/polyaxon-helper) -->
[![PyPI version](https://badge.fury.io/py/polyaxon-helper.svg)](https://badge.fury.io/py/polyaxon-helper)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](LICENCE)
[![Gitter](https://img.shields.io/gitter/room/nwjs/nw.js.svg)](https://gitter.im/polyaxon/polyaxon)

# Polyaxon-helper

Polyaxon helper is a lightweight python library to report metrics and communicate information with Polyaxon.

## Installation

```bash
$ pip install -U polyaxon-helper
```

for python3

```bash
$ pip3 install -U polyaxon-helper
```


## Install polyaxon

Please check [polyaxon installation guide](https://docs.polyaxon.com/installation/introduction)

## Install in polyaxonfile

If you want to delegate the installation to polyaxon during the build process,
add a new step to the `run` section in your polyaxonfile:

```yaml
...
run:
  image: ...
  steps:
    - ...
    - pip install -U polyaxon-helper
    - ...
  cmd: ...
```

## Usage

### Getting env variables defined by Polyaxon

```python
from polyaxon_helper import (
    get_cluster_def,
    get_declarations,
    get_experiment_info,
    get_task_info,
    get_tf_config,
    get_outputs_path,
    get_data_path,
    get_log_level
)

cluster_def = get_cluster_def()
declarations = get_declarations()
experiment_info = get_experiment_info()
task_info = get_task_info()
outputs_path = get_outputs_path()
data_path = get_data_path()
tf_config = get_tf_config()
log_level = get_log_level()
```

 * `get_cluster_def`: Returns cluster definition created by polyaxon.
    ```json
    {
        "master": ["plxjob-master0-8eefb7a1146f476ca66e3bee9b88c1de:2000"],
        "worker": ["plxjob-worker1-8eefb7a1146f476ca66e3bee9b88c1de:2000",
                   "plxjob-worker2-8eefb7a1146f476ca66e3bee9b88c1de:2000"],
        "ps": ["plxjob-master0-8eefb7a1146f476ca66e3bee9b88c1de:2000"],
    }
    ```
 * `get_declarations`: Returns all the experiment declarations based on both,

    * declarations section
    * matrix section

 * `get_experiment_info`: Returns information about the experiment.

    * project_name
    * experiment_group_name
    * experiment_name
    * project_uuid
    * experiment_group_uuid
    * experiment_uuid

 * `get_task_info`: Returns the task info: `{"type": str, "index": int}`.

 * `outputs_path`: The ouputs path generated by polyaxon based on the hierarchy of the experiment.

        `user/project/group/experiment/files`

 * `data_outputs`: The data path generated by polyaxon based on the hierarchy of the projet:

        `user/project/`

 * `get_tf_config`: Returns the TF_CONFIG defining the cluster and the current task.
    if `envvar` is not null, it will set and env variable with `envvar`.

 * `get_log_level`: If set on the polyaxonfile it will return the log level.


### Reporting metrics to Polyaxon

In order to report metrics for an experiment, just add these lines in you program.

```python
from polyaxon_helper import send_metrics

send_metrics(accuracy=0.9, precision=0.95)
```

## Quick start

Please check our [quick start guide](https://docs.polyaxon.com/quick_start) to start training your first experiment.
