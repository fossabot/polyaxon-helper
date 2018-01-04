[![Build Status](https://travis-ci.org/polyaxon/polyaxon-cli.svg?branch=master)](https://travis-ci.org/polyaxon/polyaxon-helper)
[![PyPI version](https://badge.fury.io/py/polyaxon-helper.svg)](https://badge.fury.io/py/polyaxon-helper)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](LICENCE)
[![Gitter](https://img.shields.io/gitter/room/nwjs/nw.js.svg)](https://gitter.im/polyaxon/polyaxon)

# Polyaxon-helper

A python helper library to report metrics and communicate with Polyaxon.

## Installation

```bash
$ pip install -U polyaxon-helper
```


## Install polyaxon

Please check [polyaxon installation guide](https://docs.polyaxon.com/installation/introduction)


## Usage

### Getting env variables defined by Polyaxon

```python
from polyaxon_helper import get_cluster_def, get_declarations

cluster_def = get_cluster_def()
declarations = get_declarations()
```

### Reporting metrics to Polyaxon

```python
from polyaxon_helper import send_metrics

send_metrics(accuracy=0.9, precision=0.95)
```

## Quick start

Please check our [quick start guide](https://docs.polyaxon.com/quick_start) to start training your first experiment.
