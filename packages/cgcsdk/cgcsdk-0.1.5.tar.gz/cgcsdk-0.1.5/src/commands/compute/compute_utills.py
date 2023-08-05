import click


def list_get_main_container(container_list: list, entity: str) -> dict:
    """Determines the main container of a pod.

    :param container_list: list of containers
    :type container_list: list
    :param entity: type of pod
    :type entity: str
    :return: main container
    :rtype: dict
    """
    for container in container_list:
        try:
            if container["name"] == entity:
                return container
        except KeyError:
            click.echo("something went wrong")
    return None


def list_get_mounted_volumes(volume_list: list) -> str:
    """Formats and returns list of PVC volumes mounted to a pod.

    :param volume_list: list of all volumes mounted to a pod
    :type volume_list: list
    :return: list of PVC volumes
    :rtype: str
    """
    volume_name_list = []
    for volume in volume_list:
        volume_type = volume.get("type")
        if volume_type == "PVC":
            volume_name = volume.get("name")
            volume_name_list.append(volume_name)
    volumes_mounted = (
        ", ".join(volume_name_list) if len(volume_name_list) != 0 else None
    )
    return volumes_mounted


def list_get_pod_list_to_print(pod_list: list, detailed: bool) -> list:
    """Formats and returns list of pods to print.

    :param pod_list: list of pods
    :type pod_list: list
    :return: formatted list of pods
    :rtype: list
    """
    pod_list_to_print = []
    for pod in pod_list:
        try:
            labels = pod["labels"]
            pod_name = labels["app-name"]
            pod_type = labels["entity"]
            status = pod["status"]

            gpu_type = labels.get("gpu-label")

            gpu_count = (
                labels.get("gpu-count") if labels.get("gpu-count") is not None else 0
            )

            pod_url = labels.get("pod_url")

            jupyter_token = labels.get("jupyter-token")

            main_container = list_get_main_container(pod["containers"], pod_type)

            limits = main_container["resources"].get("limits")

            cpu = limits.get("cpu") if limits is not None else 0
            ram = limits.get("memory") if limits is not None else "0Gi"

            volumes_mounted = list_get_mounted_volumes(main_container["mounts"])

            row_list = [
                pod_name,
                pod_type,
                status,
                volumes_mounted,
                cpu,
                ram,
                gpu_type,
                gpu_count,
                pod_url,
                jupyter_token,
            ]
            if not detailed:
                row_list.pop(-1)

            pod_list_to_print.append(row_list)
        except KeyError:
            pass
    return pod_list_to_print
