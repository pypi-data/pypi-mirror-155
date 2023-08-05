import click, requests, json
from tabulate import tabulate

# pylint: disable=import-error
from src.commands.compute.compute_responses import compute_create_response
from src.commands.compute.compute_responses import compute_delete_response
from src.commands.compute.data_model import compute_create_payload_validator
from src.commands.compute.data_model import compute_delete_payload_validator
from src.commands.compute.compute_utills import list_get_pod_list_to_print
from src.utils.prepare_headers import get_api_url_and_prepare_headers
from src.telemetry.basic import increment_metric
from src.telemetry.basic import setup_gauge
from src.utils.version_control import check_version
from src.utils.message_utils import prepare_error_message


@click.group("compute")
@click.option("--debug", "debug", is_flag=True, default=False, hidden=True)
@click.pass_context
def compute_group(ctx, debug):
    """
    Management of compute pods.
    """
    ctx.ensure_object(dict)
    ctx.obj["DEBUG"] = debug
    check_version()


@compute_group.command("create")
@click.argument("entity", type=click.Choice(["tensorflow-jupyter"]))
@click.option("-n", "--name", "name", type=click.STRING, required=True)
@click.option("-g", "--gpu", "gpu", type=click.IntRange(0, 8), default=0)
@click.option(
    "-gt", "--gpu-type", "gpu_type", type=click.Choice(["A100", "V100", "A5000"])
)
@click.option("-c", "--cpu", "cpu", type=click.INT, default=1)
@click.option("-m", "--memory", "memory", type=click.INT, default=2)
@click.option("-v", "--volume", "volumes", multiple=True)
def compute_create(
    entity: str,
    gpu: int,
    gpu_type: str,
    cpu: int,
    memory: int,
    volumes: list[str],
    name: str,
):
    """
    Create a compute pod in user namespace.

    :param entity: name of entity to create
    :type entity: str
    :param gpu: number of gpus to be used by pod
    :type gpu: int
    :param cpu: number of cores to be used by pod
    :type cpu: int
    :param memory: GB of memory to be used by pod
    :type memory: int
    :param volumes: list of volumes to mount
    :type volumes: list[str]
    :param name: name of pod
    :type name: str
    """
    api_url, headers = get_api_url_and_prepare_headers()
    url = f"{api_url}/v1/api/compute/create"

    payload = compute_create_payload_validator(
        name=name,
        entity=entity,
        cpu=cpu,
        memory=memory,
        gpu=gpu,
        volumes=volumes,
        gpu_type=gpu_type,
    )
    try:
        res = requests.post(
            url,
            data=json.dumps(payload),
            headers=headers,
            timeout=10,
        )
        click.echo(compute_create_response(res))
    except requests.exceptions.ReadTimeout:
        message = "Connection timed out. Try again or contact us at support@comtegra.pl"
        click.echo(prepare_error_message(message))


@compute_group.command("delete")
@click.option("-n", "--name", "name", type=click.STRING, required=True)
def compute_delete_cmd(name: str):
    """
    Delete a compute pod from user namespace.

    :param name: name of pod to delete
    :type name: str
    """
    compute_delete(name)


def compute_delete(name: str):
    """
    Delete a compute pod using backend endpoint.

    :param name: name of pod to delete
    :type name: str
    """
    api_url, headers = get_api_url_and_prepare_headers()
    url = f"{api_url}/v1/api/compute/delete"
    payload = compute_delete_payload_validator(name=name)
    try:
        res = requests.delete(
            url,
            data=json.dumps(payload),
            headers=headers,
            timeout=10,
        )
        click.echo(compute_delete_response(res))
    except requests.exceptions.ReadTimeout:
        message = "Connection timed out. Try again or contact us at support@comtegra.pl"
        click.echo(prepare_error_message(message))


@compute_group.command("list")
@click.option(
    "-d", "--detailed", "detailed", type=click.BOOL, is_flag=True, default=False
)
@click.pass_context
def compute_list(ctx, detailed: bool):
    """
    List all pods for user namespace.
    """
    api_url, headers = get_api_url_and_prepare_headers()
    url = f"{api_url}/v1/api/compute/list"
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

            increment_metric("compute.list.error")
            message = "Error occuerd while listing pods. Try again or contact us at support@comtegra.pl"
            click.echo(prepare_error_message(message))
            return

        data = response.json()
        namespace = data["details"]["namespace"]
        pod_list = data["details"]["pods_list"]

        setup_gauge(f"{namespace}.compute.count", len(pod_list))
        increment_metric(f"{namespace}.compute.list.ok")

        if not pod_list:
            click.echo("No pods to list.")
            return

        pod_list_to_print = list_get_pod_list_to_print(pod_list, detailed)

        list_headers = [
            "name",
            "type",
            "status",
            "volumes mounted",
            "CPU cores",
            "RAM",
            "GPU type",
            "GPU count",
            "URL",
            "Jupyter token",
        ]
        if not detailed:
            list_headers.remove("Jupyter token")

        if ctx.obj["DEBUG"]:
            print(pod_list_to_print)
        else:
            click.echo(tabulate(pod_list_to_print, headers=list_headers))

    except requests.exceptions.ReadTimeout:
        message = "Connection timed out. Try again or contact us at support@comtegra.pl"
        click.echo(prepare_error_message(message))
