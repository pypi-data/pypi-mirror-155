import json
import requests


# pylint: disable=import-error
from src.telemetry.basic import increment_metric
from src.telemetry.basic import change_gauge
from src.utils.message_utils import prepare_error_message, prepare_success_message


def compute_create_error_parser(error: dict) -> str:
    """Function that pases error from API for compute create command.

    :param error: Dict containing error message and further info from API.
    :type error: dict
    :return: String or dict depending on error.
    :rtype: str or dict
    """
    # TODO add errors after backend is finished
    # print(error)
    try:
        if error["reason"] == "COMPUTE_TEMPLATE_NAME_ALREADY_EXISTS":
            message = f"Template with name {error['details']['name']} already exists in namespace."
            return prepare_error_message(message)
        if error["reason"] == "PVC_NOT_FOUND":
            message = f"Volume {error['details']['pvc_name']} does not exist. Pod creation failed."
            return prepare_error_message(message)
        if error["reason"] == "COMPUTE_CREATE_FAILURE":
            message = f"Entity template {error['details']['pvc_name']} not found. Pod creation failed."
            return prepare_error_message(message)
        message = prepare_error_message(error)
        return message
    except KeyError:
        message = "An unecpected error occured. Please try again, or contact support at support@comtegra.pl."
        return prepare_error_message(message)


def compute_create_response(response: requests.Response) -> str:
    """Create response string for compute create command.

    :param response: dict object from API response.
    :type response: requests.Response
    :return: Response string.
    :rtype: str
    """
    if response.status_code == 500:
        message = "Internal Server Error. Please try again, change name of the volume or contact support at support@comtegra.pl."
        return prepare_error_message(message)
    if response.status_code == 403:
        message = "Unauthorized. Please check your API key or secret key."
        return prepare_error_message(message)

    data = json.loads(response.text)

    if response.status_code == 200:
        namespace = data["details"].get("namespace")
        compute_create_telemetry_shot_ok(namespace=namespace)
        name = data["details"].get("created_service").get("name")
        entity = data["details"].get("created_service").get("labels").get("entity")
        volumes = ",".join(data["details"].get("mounted_pvc_list"))
        try:
            jupyter_token = data["details"].get("created_template").get("jupyter_token")
        except KeyError:
            jupyter_token = None
        pod_url = data["details"].get("created_template").get("pod_url")
        # TODO bedzie wiecej entity jupyterowych
        if entity == "tensorflow-jupyter":
            message = f"{entity} Pod {name} has been created! Mounted volumes: {volumes}\nAccessible at: {pod_url}\nJupyter token: {jupyter_token}"
        else:
            message = (
                f"{entity} Pod {name} has been created! Mounted volumes: {volumes}"
            )
        return prepare_success_message(message)
    else:
        increment_metric("compute.create.error")
        error = compute_create_error_parser(data)
        return error


def compute_delete_error_parser(error: dict) -> str:
    """Function that pases error from API for compute delete command.

    :param error: Dict containing error message and further info from API.
    :type error: dict
    :return: String or dict depending on error.
    :rtype: str or dict
    """
    try:
        if error["reason"] == "NOT_DELETED_ANYTHING_IN_COMPUTE_DELETE":
            message = f"Pod with name {error['details']['name']} does not exist."
            return prepare_error_message(message)
        message = prepare_error_message(error)
        return message
    except KeyError:
        message = "An unecpected error occured. Please try again, or contact support at support@comtegra.pl."
        return prepare_error_message(message)


def compute_delete_response(response: requests.Response) -> str:
    """Create response string for compute delete command.

    :param response: dict object from API response.
    :type response: requests.Response
    :return: Response string.
    :rtype: str
    """
    if response.status_code == 500:
        message = "Internal Server Error. Please try again, change name of the volume or contact support at support@comtegra.pl."
        return prepare_error_message(message)
    if response.status_code == 403:
        message = "Unauthorized. Please check your API key or secret key."
        return prepare_error_message(message)

    data = json.loads(response.text)

    if response.status_code == 200:
        namespace = data["details"].get("namespace")
        name = data["details"].get("deleted_service").get("name")
        compute_delete_telemetry_shot_ok(namespace=namespace)
        message = f"Pod {name} successfully deleted with their service."
        return prepare_success_message(message)
    else:
        increment_metric("compute.delete.error")
        error = compute_delete_error_parser(data)
        return error


def compute_create_telemetry_shot_ok(namespace: str):
    """Function that sends telemetry for compute create command."""

    increment_metric(f"{namespace}.compute.create.ok")
    change_gauge(f"{namespace}.compute.count", 1)


def compute_delete_telemetry_shot_ok(namespace: str):
    """Function that sends telemetry for compute delete command."""

    increment_metric(f"{namespace}.compute.delete.ok")
    change_gauge(f"{namespace}.compute.count", -1)
