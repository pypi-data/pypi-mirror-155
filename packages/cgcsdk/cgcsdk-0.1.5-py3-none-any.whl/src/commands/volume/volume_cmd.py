import json
import click
import requests
from tabulate import tabulate

# pylint: disable=import-error
from src.utils.prepare_headers import get_api_url_and_prepare_headers
from src.telemetry.basic import increment_metric, setup_gauge
from src.commands.volume.data_model import (
    volume_create_payload_validator,
    volume_delete_payload_validator,
    volume_mount_payload_validator,
    volume_umount_payload_validator,
)
from src.commands.volume.volume_utils import get_formatted_volume_list_and_total_size
from src.commands.volume.volume_responses import (
    volume_response_parser,
    volume_create_response,
    volume_delete_response,
)
from src.utils.version_control import check_version
from src.utils.message_utils import prepare_error_message


@click.group("volume")
@click.option("--debug", "debug", is_flag=True, default=False, hidden=True)
@click.pass_context
def volume_group(ctx, debug):
    """
    Management of volumes.
    """
    # pylint: disable=unnecessary-pass
    ctx.ensure_object(dict)
    ctx.obj["DEBUG"] = debug
    check_version()


@volume_group.command("list")
@click.pass_context
def volume_list(ctx):
    """
    List all volumes for user namespace.
    """
    api_url, headers = get_api_url_and_prepare_headers()
    url = f"{api_url}/v1/api/storage/volume/list"
    try:
        response = requests.get(
            url=url,
            headers=headers,
            timeout=10,
        )

        if response.status_code != 200:
            if response.status_code == 403:
                message = "Unauthorized. Please check your API key or secret key."
                click.echo(prepare_error_message(message))
                return
            increment_metric("volume.list.error")
            message = "Error occuerd while listing volumes. Try again or contact us at support@comtegra.pl"
            click.echo(prepare_error_message(message))
            return

        data = response.json()
        list_of_volumes = data["details"]["volume_list"]
        namespace = data["details"]["namespace"]

        increment_metric(f"{namespace}.volume.list.ok")
        setup_gauge(f"{namespace}.volume.count", len(list_of_volumes))

        if not list_of_volumes:
            click.echo("No volumes to list.")
            return

        volume_list_to_print, total_size = get_formatted_volume_list_and_total_size(
            list_of_volumes
        )
        list_headers = ["name", "used", "size", "type", "mounted to"]
        setup_gauge(f"{namespace}.volume.totalSizeAccumulated", total_size)

        if ctx.obj["DEBUG"]:
            click.echo(volume_list_to_print)
        else:
            click.echo(tabulate(volume_list_to_print, headers=list_headers))

    except requests.exceptions.ReadTimeout:
        message = "Connection timed out. Try again or contact us at support@comtegra.pl"
        click.echo(prepare_error_message(message))


@volume_group.command("create")
# create `<name>*` --size* <int GB> --type <HDD|SSD*> --access <RWO|RWX\*>
@click.argument("name")
# TODO exception on limit excess - backend
@click.option("-s", "--size", "size", type=click.IntRange(1, 1000), required=True)
@click.option(
    "-t", "--type", "disk_type", type=click.Choice(["hdd", "ssd"]), default="ssd"
)
@click.option("-a", "--a", "access", type=click.Choice(["rwx", "rwo"]), default="rwx")
def volume_create(name: str, size: int, disk_type: str, access: str):
    """Create volume in user namespace.

    :param name: name of volume
    :type name: str
    :param size: size of volume in GB
    :type size: int
    :param type: type of volume - HDD or SSD
    :type type: str
    :param access: access type of volume - RWO or RWX
    :type access: str
    """
    api_url, headers = get_api_url_and_prepare_headers()
    url = f"{api_url}/v1/api/storage/volume/create"
    payload = volume_create_payload_validator(
        name=name,
        access=access,
        size=size,
        disk_type=disk_type,
    )
    try:
        res = requests.post(
            url,
            data=json.dumps(payload),
            headers=headers,
            timeout=10,
        )
        click.echo(volume_create_response(res))

    except requests.exceptions.ReadTimeout:
        message = "Connection timed out. Try again or contact us at support@comtegra.pl"
        click.echo(prepare_error_message(message))


@volume_group.command("delete")
# {  "name": "test-volume",  "force_delete": true }
@click.argument("name")
@click.option("-f", "--force", "force_delete", is_flag=True, default=False)
def volume_delete(name: str, force_delete: bool):
    """Delete specific volume from user namespace.

    :param name: name of the volume to delete
    :type name: str
    :param force_delete: delete volume even if it is still mounted
    :type force_delete: bool
    """
    api_url, headers = get_api_url_and_prepare_headers()
    url = f"{api_url}/v1/api/storage/volume/delete"
    payload = volume_delete_payload_validator(
        name=name,
        force_delete=force_delete,
    )
    try:
        res = requests.delete(
            url,
            data=json.dumps(payload),
            headers=headers,
            timeout=10,
        )

        click.echo(volume_delete_response(res))

    except requests.exceptions.ReadTimeout:
        message = "Connection timed out. Try again or contact us at support@comtegra.pl"
        click.echo(prepare_error_message(message))


@volume_group.command("umount")
@click.argument("name")
def volume_umount(name: str):
    """Umount volume from compute resources.

    :param name: name of the volume to umount
    :type name: str
    """
    api_url, headers = get_api_url_and_prepare_headers()
    url = f"{api_url}/v1/api/storage/volume/umount"
    payload = volume_umount_payload_validator(name=name)

    try:
        res = requests.post(
            url,
            data=json.dumps(payload),
            headers=headers,
            timeout=10,
        )
        click.echo(volume_response_parser(res, "umount"))

    except requests.exceptions.ReadTimeout:
        message = "Connection timed out. Try again or contact us at support@comtegra.pl"
        click.echo(prepare_error_message(message))


@volume_group.command("mount")
# {  "name": "test-volume", "target_template_name": "jupyter-notebook", "start_mount_path": "/tf" }
@click.argument("name")
@click.option("-t", "--target", "target", type=str, required=True)
@click.option(
    "-ttt",
    "--target_template_type",
    "target_template_type",
    type=click.Choice(["deployment"]),
)
@click.option("-p", "--mount_path", "mount_path", type=str, default="/tf")
def volume_mount(
    name: str,
    target_template_type: str,
    target: str,
    mount_path: str,
):
    """Mount volume to specific template.

    :param name: name of the volume to mount
    :type name: str
    :param target_template_type: type of template to mount volume to
    :type target_template_type: str
    :param target: name of the template to mount volume to
    :type target: str
    :param mount_path: path to mount volume to
    :type mount_path: str
    """
    api_url, headers = get_api_url_and_prepare_headers()
    url = f"{api_url}/v1/api/storage/volume/mount"
    payload = volume_mount_payload_validator(
        name=name,
        target=target,
        target_template_type=target_template_type,
        mount_path=mount_path,
    )
    try:
        res = requests.post(
            url,
            data=json.dumps(payload),
            headers=headers,
            timeout=10,
        )

        click.echo(volume_response_parser(res, "mount"))

    except requests.exceptions.ReadTimeout:
        message = "Connection timed out. Try again or contact us at support@comtegra.pl"
        click.echo(prepare_error_message(message))
