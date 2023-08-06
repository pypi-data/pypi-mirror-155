from __future__ import annotations

import pandas as pd
import functools
import os
from dataclasses import dataclass
from typing import Any, Union
from pathlib import Path
from typing import List, Optional, Union, Any
from pydantic import BaseModel, dataclasses, fields, Field
import yaml
import json
import os
import dataclasses
from typing import Union, Dict, Any, TypedDict
from pathlib import Path

from aws_pcluster_helpers import (PClusterConfig, InstanceTypesData, PClusterInstanceTypes, InstanceTypesMappings,
                                  size_in_gib)
from aws_pcluster_helpers.utils.logging import setup_logger
from aws_pcluster_helpers.models.config import PClusterConfigFiles
from rich.console import Console
from rich.table import Table

logger = setup_logger(logger_name='sinfo')


@dataclasses.dataclass
class SinfoRow:
    sinfo_name: str
    label: str
    queue: str
    constraint: str
    ec2_instance_type: str
    mem: int
    cpu: int
    gpu: Optional[dict]
    gpus: Optional[List]
    extra: Optional[dict]


# TODO add custom ami lookup

@dataclass
class SInfoTable:

    @functools.cached_property
    def table_columns(self) -> List[Any]:
        return [
            {'label': 'Queue', 'key': 'queue'},
            {'label': 'Constraint', 'key': 'constraint'},
            {'label': 'Mem(Gib)', 'key': 'mem'},
            {'label': 'CPU', 'key': 'cpu'},
            {'label': 'EC2', 'key': 'ec2_instance_type'},
        ]

    @functools.cached_property
    def pcluster_config_files(self) -> PClusterConfigFiles:
        return PClusterConfigFiles()

    @functools.cached_property
    def instance_type_mappings(self) -> InstanceTypesMappings:
        return InstanceTypesMappings.from_json(
            self.pcluster_config_files.instance_name_type_mappings_file)

    @functools.cached_property
    def pcluster_instance_types(self) -> PClusterInstanceTypes:
        return PClusterInstanceTypes.from_json(self.pcluster_config_files.instance_types_data_file)

    @functools.cached_property
    def pcluster_config(self) -> PClusterConfig:
        return PClusterConfig.from_yaml(self.pcluster_config_files.pcluster_config_file)

    @functools.cached_property
    def rows(self) -> List[SinfoRow]:
        instance_types_mappings = self.instance_type_mappings
        pcluster_instance_types = self.pcluster_instance_types

        sinfo_records = []
        for slurm_queue in self.pcluster_config.Scheduling.SlurmQueues:
            compute_resources = slurm_queue.ComputeResources
            queue = slurm_queue.Name
            for compute_resource in compute_resources:
                sinfo_label = {}
                sinfo_instance_type = compute_resource.Name
                ec2_instance_type = instance_types_mappings.sinfo_instance_types[sinfo_instance_type][
                    'ec2_instance_type']
                pcluster_instance_type = pcluster_instance_types.instance_type_data.get(ec2_instance_type)
                mem_in_mib = pcluster_instance_type.data['data']['MemoryInfo']['SizeInMiB']
                mem_in_gib = size_in_gib(mem_in_mib)
                cpu = pcluster_instance_type.data['data']['VCpuInfo']['DefaultCores']
                gpu = None
                gpus = []
                if 'GpuInfo' in pcluster_instance_type.data['data']:
                    gpu = pcluster_instance_type.data['data']['GpuInfo']
                    gpu_total_mem_in_mib = gpu["TotalGpuMemoryInMiB"]
                    gpu_total_mem_in_gib = size_in_gib(gpu_total_mem_in_mib)
                    gpus.append(gpu)
                cpu = pcluster_instance_type.data['data']['VCpuInfo']['DefaultCores']
                p_type = 'dy'
                if compute_resource.MinCount > 0:
                    p_type = 'st'
                label = f"{slurm_queue.Name.replace('-', '_')}_{p_type}__{ec2_instance_type.replace('.', '_')}"
                sinfo_name = f"{slurm_queue.Name}-{p_type}-{sinfo_instance_type}"

                sinfo_label['name'] = label
                sinfo_label['max_mem'] = int(mem_in_gib)
                sinfo_label['max_cpu'] = cpu
                sinfo_label['queue'] = queue
                sinfo_label['constraint'] = sinfo_instance_type
                sinfo_records.append(
                    SinfoRow(
                        mem=int(mem_in_gib),
                        cpu=cpu,
                        sinfo_name=sinfo_name,
                        queue=queue,
                        constraint=sinfo_instance_type,
                        ec2_instance_type=ec2_instance_type,
                        label=label,
                        gpus=gpus,
                        extra={},
                        gpu=None,
                    )
                )
        return sinfo_records

    @functools.cached_property
    def dataframe(self) -> pd.DataFrame:
        records = []
        for record in self.rows:
            records.append(record.__dict__)
        df = pd.DataFrame.from_records(records)
        df.sort_values(by=['queue', 'mem', 'cpu'], inplace=True)
        return df

    def get_table(self):
        if not len(self.rows):
            logger.error(f'SLURM SInfo - none found... exiting')
            raise ValueError(f'SLURM SInfo - none found ... exiting')

        table = Table(title="SLURM SInfo", show_lines=True)
        colors = ["turquoise4", "purple4", "deep_sky_blue3", "hot_pink3", "dodger_blue1"]
        queue_colors = {}
        for column in self.table_columns:
            table.add_column(column['label'], justify="right", no_wrap=True)
        table.add_column('SBATCH', justify="left")
        for row in self.dataframe.to_records():
            t_row = []
            if row['queue'] not in queue_colors:
                queue_colors[row['queue']] = colors.pop()
            queue = row['queue']
            constraint = row['constraint']
            cpus = row['cpu']
            color = queue_colors[row['queue']]
            for t in self.table_columns:
                key = t['key']
                value = row[key]
                t_row.append(f"[{color}]{str(value)}")
            t_row.append(
                f"[{color}]#SBATCH --partition={queue}\n#SBATCH --constraint={constraint}\n#SBATCH -c={cpus}")
            table.add_row(*t_row)

        return table
