# uncompyle6 version 3.7.4
# Python bytecode 3.7 (3394)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/allrank/utils/file_utils.py
# Compiled at: 2020-03-04 08:08:01
# Size of source mod 2**32: 1972 bytes
import os
from typing import Any
from urllib.parse import urlparse
import gcsfs
from attr import attrib, attrs
from pkg_resources import Requirement, resource_filename
from allrank.utils.command_executor import execute_command
from allrank.utils.ltr_logging import get_logger
logger = get_logger()

@attrs
class PathsContainer:
    base_output_path = attrib(type=str)
    output_dir = attrib(type=str)
    tensorboard_output_path = attrib(type=str)
    config_path = attrib(type=str)

    @classmethod
    def from_args(cls, output, run_id, config_path, package_name='allrank'):
        base_output_path = get_path_from_local_uri(output)
        output_dir = os.path.join(base_output_path, 'results', run_id)
        tensorboard_output_path = os.path.join(base_output_path, 'tb_evals', 'single', run_id)
        if not os.path.exists(config_path):
            print('config not exists at {}, extracting config file path from package {}'.format(config_path, package_name))
            config_path = resource_filename(Requirement.parse(package_name), os.path.join(package_name, config_path))
        print('will read config from {}'.format(config_path))
        return cls(base_output_path, output_dir, tensorboard_output_path, config_path)


def clean_up(path):
    rm_command = 'rm -rf {path}'.format(path=path)
    execute_command(rm_command)


def create_output_dirs(output_path: str) -> None:
    for subdir in ('models', 'models/partial', 'evals', 'evals/tensorboard', 'predictions'):
        os.makedirs((os.path.join(output_path, subdir)), exist_ok=True)


def get_path_from_local_uri(uri: Any) -> str:
    parsed = urlparse(uri)
    if parsed.scheme == 'file':
        return parsed.netloc + parsed.path
    return uri


def is_gs_path(uri) -> bool:
    return urlparse(uri).scheme == 'gs'


def open_local_or_gs(path, mode):
    open_func = gcsfs.GCSFileSystem().open if is_gs_path(path) else open
    return open_func(path, mode)