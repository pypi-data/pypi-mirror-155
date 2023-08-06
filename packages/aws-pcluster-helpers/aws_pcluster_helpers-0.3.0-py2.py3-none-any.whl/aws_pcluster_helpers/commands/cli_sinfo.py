import os
from aws_pcluster_helpers.models.sinfo import SInfoTable, SinfoRow
from aws_pcluster_helpers.models import nextflow
from rich.console import Console
from rich.table import Table


def main():
    sinfo = SInfoTable()
    table = sinfo.get_table()
    console = Console()
    console.print(table)
