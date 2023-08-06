# Copyright 2019-2022 DADoES, Inc.
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License in the root directory in the "LICENSE" file or at:
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.
from cmath import log
import os
import logging
import importlib
import anatools.lib.context as ctx

logger = logging.getLogger(__name__)

def get_volume_path(package, inpath):
    """
    Convert a volume path to an absolute path
    Deprecated - use get_data_path instead
    """
    if ":" in inpath:
        # path includes a volume
        volume_name, rel_path = inpath.split(":")
        volume_path = ctx.packages[package]['volumes'][volume_name]
        if os.path.isabs(volume_path):
            # volume is an absolute path
            return os.path.join(volume_path, rel_path)
        else:
            # volume is relative to "--data" parameter
            print(volume_path)
            if volume_path == 'local':
                return os.path.join(ctx.data, 'local', volume_name, rel_path)
            else: 
                return os.path.join(ctx.data, 'volumes', volume_path, rel_path)
    else:
        # path does not include a volume
        if os.path.isabs(inpath):
            # path is absolute
            return inpath
        else:
            # path is relative to "--data" parameter
            return os.path.join(ctx.data, inpath)

def get_file_path(package, inpath):
    """
    Convert a filename path to an absolute path
    """
    if ":" in inpath:
        # path includes a logical component
        logical_name, rel_path = inpath.split(":")
        if "volumes" in ctx.packages[package] and logical_name in ctx.packages[package]['volumes']:
            # logical path is a volume
            volume_path = ctx.packages[package]['volumes'][logical_name]
            if os.path.isabs(volume_path):
                # volume is an absolute path
                return os.path.join(volume_path, rel_path)
            else:
                # volume is relative to "--data" parameter
                if volume_path == 'local':
                    return os.path.join(ctx.data, 'local', logical_name, rel_path)
                else: 
                    return os.path.join(ctx.data, 'volumes', volume_path, rel_path)
        elif "package_data" in ctx.packages[package] and logical_name in ctx.packages[package]['package_data']:
            package_path = ctx.packages[package]['package_data'][logical_name]
            package_module = importlib.import_module(package)
            package_init = package_module.__file__
            package_dir = os.path.dirname(os.path.realpath(package_init))
            return os.path.join(package_dir, package_path, rel_path)
        else:
            logger.critical(f"Logical name '{logical_name}' in package '{package}' not found")
            raise ValueError
    else:
        # path does not include a logical component
        if os.path.isabs(inpath):
            # path is absolute
            return inpath
        else:
            # path is relative to "--data" parameter
            return os.path.join(ctx.data, inpath)
