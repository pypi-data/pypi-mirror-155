from __future__ import annotations
import functools
import os

from jinja2 import Environment, BaseLoader
from pydantic.dataclasses import dataclass
import dataclasses
from typing import List, Any, TypedDict, Dict, Optional
from typing import ForwardRef
from devtools import PrettyFormat, pprint, pformat, debug
import json
import yaml

from aws_pcluster_helpers import (PClusterConfig, InstanceTypesData, PClusterInstanceTypes, InstanceTypesMappings,
                                  size_in_gib)

from aws_pcluster_helpers.models.instance_types_data import (PClusterInstanceTypes, InstanceTypesMappings)

from aws_pcluster_helpers.models import sinfo
from aws_pcluster_helpers import (PClusterConfig, InstanceTypesData, PClusterInstanceTypes, InstanceTypesMappings,
                                  size_in_gib)
from aws_pcluster_helpers.utils.logging import setup_logger
from aws_pcluster_helpers.models.config import PClusterConfigFiles


# NXFProcess = ForwardRef('NXFProcess')


@dataclasses.dataclass
class NXFProcess(sinfo.SinfoRow):
    mem_min: int = 1
    cpu_min: int = 1


defaults = {
    'queue': None,
    'sinfo_name': None,
    'constraint': None,
    'ec2_instance_type': None,
    'gpus': None,
    'gpu': None,
    'extra': None
}


@dataclass
class NXFSlurmConfig(sinfo.SInfoTable):

    @functools.cached_property
    def processes(self) -> Dict[str, NXFProcess]:
        t_processes = {}
        for row in self.rows:
            row_data = row.__dict__
            label = row_data['label']
            t_processes[label] = NXFProcess(**row_data)
        return t_processes

    @functools.cached_property
    def default_processes(self) -> Dict[str, NXFProcess]:
        return {
            'tiny': NXFProcess(label='tiny',
                               mem_min=1, mem=6, cpu=1, **defaults),
            'low': NXFProcess(label='low', mem_min=2, cpu_min=1, mem=12, cpu=2, **defaults),
            'medium': NXFProcess(label='medium', mem_min=12, cpu_min=1, mem=36, cpu=6, **defaults),
            'high': NXFProcess(label='high', mem_min=36, cpu_min=6, mem=72, cpu=12, **defaults),
            'high_mem': NXFProcess(label='high_memory', mem_min=72, cpu_min=12, mem=200, cpu=12,
                                   **defaults),
            'long': NXFProcess(label='long', mem_min=12, cpu_min=1, mem=36, cpu=6, **defaults),
        }

    def map_nxf_default_labels_to_pcluster_queues(self):
        for key in self.default_processes.keys():
            # this doesn't take cpu into account...
            best_match = min(list(self.processes.keys()),
                             key=lambda x: abs(self.processes[x].mem - self.default_processes[key].mem))
            self.default_processes[key].queue = self.processes[best_match].queue
            self.default_processes[key].constraint = self.processes[best_match].constraint

    def __post_init__(self):
        self.map_nxf_default_labels_to_pcluster_queues()
        return

    def print_slurm_config(self):
        config_template_file = os.path.join(os.path.dirname(__file__), '_templates', 'slurm.config')
        if not os.path.exists(config_template_file):
            raise ValueError(f'Config template does not exist')
        with open(config_template_file, 'r+') as f:
            config_template = f.read()
        rtemplate = Environment(loader=BaseLoader).from_string(config_template)
        data = {
            'processes': self.processes,
            'default_processes': self.default_processes
        }
        return rtemplate.render(**data)
