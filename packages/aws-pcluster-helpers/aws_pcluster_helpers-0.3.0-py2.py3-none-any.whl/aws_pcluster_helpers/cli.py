import rich_click as click
from rich_click import RichCommand, RichGroup

from aws_pcluster_helpers.commands import cli_sinfo
from aws_pcluster_helpers.commands import cli_gen_nxf_slurm_config


@click.group()
def cli():
    """
    Helper functions for aws parallelcluster.
    """
    return


@cli.command()
def sinfo():
    """
    A more helpful sinfo
    """
    click.echo("Printing sinfo table")
    cli_sinfo.main()


@cli.command()
@click.option("--output", "-o", help="Output path", required=False)
@click.option("--overwrite", is_flag=True, help="Overwrite local files")
@click.option("--stdout", is_flag=True, help="Write slurm config to stdout")
def gen_nxf_slurm_config(output: str, overwrite: bool, stdout: bool):
    """
    Generate a slurm.config for nextflow that is compatible with your cluster.

    You will see a process label for each partition/node type.

    Use the configuration in your process by setting the label to match the label in the config.
    """
    click.echo("Generating NXF Slurm config")
    cli_gen_nxf_slurm_config.main(output, overwrite, stdout)


if __name__ == "__main__":
    cli()
