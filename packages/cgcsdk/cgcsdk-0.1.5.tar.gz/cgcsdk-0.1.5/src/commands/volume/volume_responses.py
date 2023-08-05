import json
import requests

# pylint: disable=import-error
from src.telemetry.basic import increment_metric, change_gauge
from src.utils.message_utils import prepare_error_message
from src.utils.message_utils import prepare_success_message
from src.utils.message_utils import prepare_warning_message


def volume_create_error_parser(error: dict) -> str:
    """Function that pases error from API for volume create command.
    For now there is two errors implementned to give string output.

    :param error: Dict containing error message and further info from API.
    :type error: dict
    :return: String or dict depending on error.
    :rtype: str or dict
    """

    try:
        if error["reason"] == "AlreadyExists":
            message = f"Volume with name {error['details']['name']} already exists."
            return prepare_error_message(message)
        if error["reason"] == "PVC_CREATE_NO_SC":
            message = f"Volume {error['details']['name']} could not be created. No storage class defined for this access type."
            return prepare_error_message(message)
        if error["reason"] == "PVC_CREATE_MOUNT_FAILURE":
            message = "PVC created successfully but Filebrowser deployment is not existing in namespace."
            return prepare_warning_message(message)
        message = error["reason"]
        return prepare_error_message(message)
    except KeyError:
        message = "An unexpected error occured. Please try again, change name of the volume or contact support at support@comtegra.pl."
        return prepare_error_message(message)


def volume_create_response(response: requests.Response) -> str:
    """Create response string for volume create command.

    :param response: dict object from API response.
    :type response: requests.Response
    :return: Response string.
    :rtype: str
    """

    if response.status_code == 500:
        message = "Internal Server Error. Please try again, change name of the volume or contact support at support@comtegra.pl."
        return prepare_error_message(message)
    if response.status_code == 401:
        message = "Could not validate user id or access key"
        return prepare_error_message(message)

    data = json.loads(response.text)

    def shoot_telemetry(size: int, namespace: str):
        """Function that sends telemetry for volume create command.
        Created only because occured error 201. We don't know all the errors yet. 201 creates volume but fires excepion"""
        increment_metric(f"{namespace}.volume.create.ok")
        change_gauge(f"{namespace}.volume.count", 1)
        change_gauge(f"{namespace}.volume.totalSizeAccumulated", size)

    if response.status_code == 200:
        namespace = data["details"]["namespace"]
        name = data["details"]["volume_created"]["name"]
        size = data["details"]["volume_created"]["size"]
        access = data["details"]["volume_created"]["access_type"][0]
        disk_type = data["details"]["volume_created"]["disks_type"]
        shoot_telemetry(int("".join(filter(str.isdigit, size))), namespace)
        message = f"Volume {name} of size {size} GB on {disk_type} created from imported module. Volume is {access}."
        return prepare_success_message(message)

    if response.status_code == 202:
        error = volume_create_error_parser(data)
        size = data["details"]["volume_created"]["size"]
        shoot_telemetry(int("".join(filter(str.isdigit, size))), namespace)
        return error

    else:
        increment_metric("volume.create.error")
        error = volume_create_error_parser(data)
        return error


def volume_delete_error_parser(error: dict) -> str:
    """Function that pases error from API for volume delete command.
    For now there is one error implementned to give string output.

    :param error: Dict containing error message and further info from API.
    :type error: dict
    :return: String or dict depending on error.
    :rtype: str or dict
    """

    try:
        if error["reason"] == "NotFound":
            message = f"Volume {error['details']['name']} not found."
            return prepare_error_message(message)
        if error["reason"] == "PVC_DELETE_EXCEPTION":
            message = f"Volume {error['details']['pvc_name']} is still mounted. Please unmount it or use the --force flag."
            return prepare_error_message(message)
        message = error["reason"]
        return prepare_error_message(message)
    except KeyError:
        message = "An unexpected error occured. Please try again, change name of the volume or contact support at support@comtegra.pl."
        return prepare_error_message(message)


def volume_delete_response(response: requests.Response) -> str:
    """Create response string for volume delete command.

    :param response: dict object from API response.
    :type response: requests.Response
    :return: Response string.
    :rtype: str
    """
    if response.status_code == 500:
        message = "Internal Server Error. Please try again, or contact support at support@comtegra.pl."
        return prepare_error_message(message)
    if response.status_code == 403:
        message = "Unauthorized. Please check your API key or secret key."
        return prepare_error_message(message)

    data = json.loads(response.text)

    if response.status_code == 200:
        namespace = data["details"]["namespace"]
        name = data["details"]["volume_deleted"]["name"]
        size = int(
            "".join(filter(str.isdigit, data["details"]["volume_deleted"]["size"]))
        )
        increment_metric(f"{namespace}.volume.delete.ok")
        change_gauge(f"{namespace}.volume.count", -1)
        change_gauge(f"{namespace}.volume.totalSizeAccumulated", -size)

        message = f"Volume {name} deleted."
        return prepare_success_message(message)
    increment_metric("volume.delete.error")
    # TODO other errors if implemented
    error = volume_delete_error_parser(data)
    return error


def volume_response_parser(response: requests.Response, command: str) -> str:
    """Response parser for volume mount and umount.

    :param response: response to parse.
    :type response: requests.Response
    :return: response message string.
    :rtype: str
    """
    if response.status_code == 403:
        message = "Unauthorized. Please check your API key or secret key."
        return prepare_error_message(message)
    try:
        data = json.loads(response.text)
        server_message = data["message"]
        namespace = data["details"]["namespace"]

        if response.status_code == 200:
            increment_metric(f"{namespace}.volume.{command}.ok")
            message = prepare_success_message(server_message)
        else:
            increment_metric(f"{namespace}.volume.{command}.error")
            message = prepare_error_message(server_message)
        return message
    except KeyError:
        increment_metric(f"volume.{command}.error")
        message = "Unknown error occured. Please contact support at support@comtegra.pl"
        return prepare_error_message(message)
    except json.JSONDecodeError:
        increment_metric(f"volume.{command}.error")
        message = "Unknown error occured. Please contact support at support@comtegra.pl"
        return prepare_error_message(message)
