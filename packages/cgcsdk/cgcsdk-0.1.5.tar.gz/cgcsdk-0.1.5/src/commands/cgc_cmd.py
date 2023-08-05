import click

# pylint: disable=import-error
from src.commands.compute.compute_cmd import compute_delete
from src.utils.version_control import check_version


@click.command("rm")
@click.option("-n", "--name", "name", type=click.STRING, required=True)
def cgc_rm(name: str):
    """
    Delete a compute pod in user namespace

    :param name: name of pod to delete
    :type name: str
    """
    check_version()
    compute_delete(name)
