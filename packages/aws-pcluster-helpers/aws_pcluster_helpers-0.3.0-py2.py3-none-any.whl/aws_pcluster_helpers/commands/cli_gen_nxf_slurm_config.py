import os
from aws_pcluster_helpers.models.sinfo import SInfoTable, SinfoRow
from aws_pcluster_helpers.models import nextflow
from rich.console import Console
from rich.table import Table
import sys

from aws_pcluster_helpers.utils.logging import setup_logger

logger = setup_logger('nxf')


def main(outfile, overwrite, stdout):
    nxf_slurm_config = nextflow.NXFSlurmConfig()
    data = nxf_slurm_config.print_slurm_config()
    if outfile:
        if os.path.exists(outfile) and not overwrite:
            logger.warn(
                f'Outfile: {outfile} exists. Please specify --overwrite print your config or select a file that does not exist.')
            sys.exit(1)
        with open(outfile, 'w') as fh:
            fh.write(data)
    if stdout:
        print(data)
    else:
        logger.warn(f'Neither --outfile or --stdout were selected. Printing to the screen anyways.')
        print(data)
