#!/usr/bin/env python

"""Tests for `aws_pcluster_helpers` package."""

import unittest

from aws_pcluster_helpers import (PClusterConfig, PClusterConfigFiles, InstanceTypesData, PClusterInstanceTypes,
                                  InstanceTypesMappings,
                                  size_in_gib)
from aws_pcluster_helpers.utils.logging import setup_logger
from aws_pcluster_helpers.models.config import (ENV_PCLUSTER_CONFIG_FILE, ENV_INSTANCE_TYPES_DATA_FILE,
                                                ENV_INSTANCE_TYPE_MAPPINGS_FILE)
import yaml
import json
import os
from devtools import PrettyFormat, pprint, pformat, debug

instance_types_data_file = os.path.join(os.path.dirname(__file__), 'instance-types-data.json')
instance_type_mapping_file = os.path.join(os.path.dirname(__file__), 'instance_name_type_mappings.json')
pcluster_config_file = os.path.join(os.path.dirname(__file__), 'pcluster_config.yml')
os.environ[ENV_INSTANCE_TYPE_MAPPINGS_FILE] = instance_type_mapping_file
os.environ[ENV_INSTANCE_TYPES_DATA_FILE] = instance_types_data_file
os.environ[ENV_PCLUSTER_CONFIG_FILE] = pcluster_config_file

logger = setup_logger(logger_name='tests', log_level='DEBUG')


def test_load_pcluster_config():
    pcluster_config = PClusterConfig.from_yaml(pcluster_config_file)
    assert pcluster_config


def test_load_instance_types_data():
    pcluster_instance_types = PClusterInstanceTypes.from_json(instance_types_data_file)
    debug(pcluster_instance_types)
    assert pcluster_instance_types


def test_load_instance_types_mapping():
    instance_types_mappings = InstanceTypesMappings.from_json(instance_type_mapping_file)
    assert instance_types_mappings


def test_nxf_gen():
    instance_types_mappings = InstanceTypesMappings.from_json(instance_type_mapping_file)
    pcluster_instance_types = PClusterInstanceTypes.from_json(instance_types_data_file)
    pcluster_config = PClusterConfig.from_yaml(pcluster_config_file)
    return


def test_pcluster_config_files():
    pcluster_config_files = PClusterConfigFiles()
