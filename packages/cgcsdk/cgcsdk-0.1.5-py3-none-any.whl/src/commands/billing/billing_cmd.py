import click, os, pkg_resources
from dotenv import load_dotenv


env_file = pkg_resources.resource_filename("src", ".env")
load_dotenv(dotenv_path=env_file, verbose=True)


API_URL = os.getenv("API_URL")
CGC_SECRET = os.getenv("CGC_SECRET")


@click.group("billing")
def billing_group():
    """
    Access and manage billing information.
    """
    pass


@billing_group.command("status")
def billing_status():
    """
    Shows billing status for user namespace
    """
    click.echo("Showing billing status!")


@billing_group.command("pay")
def billing_pay():
    """
    Interface for easy payment
    """
    click.echo("Initializing payment!")


@click.group("fvat")
def fvat_group():
    """
    Invoice management
    """
    pass


@fvat_group.command("ls")
def fvat_ls():
    """
    Lists all invoices for user namespace
    """
    click.echo("Listing all invoices!")


@fvat_group.command("id")
@click.argument(
    "invoice_id",
)
def fvat_id(invoice_id: str):
    """
    Opens invoice with given ID
    """
    click.echo(f"Opening invoice {invoice_id}!")


billing_group.add_command(fvat_group)
