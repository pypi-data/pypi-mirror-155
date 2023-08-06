from __future__ import annotations
import os
from dataclasses import dataclass
from typing import Any, Union
from pathlib import Path
from typing import List
from pydantic import BaseModel, dataclasses, fields
import yaml
import json
import os
import dataclasses
from typing import Union, Dict, Any, TypedDict
from pathlib import Path

ENV_PCLUSTER_CONFIG_FILE = 'PCLUSTER_CONFIG_FILE'
ENV_INSTANCE_TYPE_MAPPINGS_FILE = 'INSTANCE_TYPE_MAPPINGS_FILE'
ENV_INSTANCE_TYPES_DATA_FILE = 'INSTANCE_TYPES_DATA_FILE'


@dataclasses.dataclass
class PClusterConfigFiles:
    @property
    def pcluster_config_file(self) -> Union[str, Path]:
        return os.environ.get(ENV_PCLUSTER_CONFIG_FILE,
                              '/opt/parallelcluster/shared/cluster-config.yaml')

    @property
    def instance_name_type_mappings_file(self) -> Union[str, Path]:
        return os.environ.get(ENV_INSTANCE_TYPE_MAPPINGS_FILE,
                              '/opt/slurm/etc/pcluster/instance_name_type_mappings.json')

    @property
    def instance_types_data_file(self) -> Union[str, Path]:
        return os.environ.get(ENV_INSTANCE_TYPES_DATA_FILE,
                              '/opt/parallelcluster/shared/instance-types-data.json')
