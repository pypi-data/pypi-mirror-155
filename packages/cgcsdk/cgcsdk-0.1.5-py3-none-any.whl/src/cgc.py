import click

# pylint: disable=import-error
from src.commands.volume.volume_cmd import volume_group
from src.commands.compute.compute_cmd import compute_group
from src.commands.billing.billing_cmd import billing_group
from src.commands.auth.auth_cmd import auth_register
from src.commands.cgc_cmd import cgc_rm


@click.group()
def cli():
    """Function to group all the commands."""
    pass


cli.add_command(volume_group)
cli.add_command(compute_group)
cli.add_command(billing_group)
cli.add_command(auth_register)
cli.add_command(cgc_rm)


if __name__ == "__main__" or __name__ == "src.cgc":
    cli()
else:
    raise Exception("This program is not intended for importing!")
