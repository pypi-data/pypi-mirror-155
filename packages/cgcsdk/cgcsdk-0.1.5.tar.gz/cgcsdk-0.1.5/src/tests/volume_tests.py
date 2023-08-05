import ast
from click.testing import CliRunner


# pylint: disable=import-error
from src.commands.volume.volume_cmd import volume_group


def test_volume_list(volume=""):
    """Module for testing volume list command

    :param volume: name of voulme, defaults to ""
    :type volume: str, optional
    """
    runner = CliRunner()
    result = runner.invoke(volume_group, ["--debug", "list"])

    if volume == "":
        assert (
            result.output.strip() == "No volumes to list."
        ), "VOLUME LIST TEST FAILED1"
    else:
        data = ast.literal_eval(result.output.strip())
        assert (
            len(data) == 1 and volume in data[0] and "1Gi" in data[0]
        ), "VOLUME LIST TEST FAILED2"
    print("VOLUME LIST TEST OK")


def test_volume_create(volume):
    """Module for testing volume create command

    :param volume: name of voulme
    :type volume: str
    """
    runner = CliRunner()
    result = runner.invoke(volume_group, ["create", volume, "--size", 1])
    assert (
        f"Success: Volume {volume} of size 1Gi GB on SSD created from imported module. Volume is ReadWriteMany."
        in result.output.strip()
    ), "VOLUME CREATE TEST FAILED"
    print("VOLUME CREATE TEST OK")


def test_volume_delete(volume):
    """Module for testing volume delete command

    :param volume: name of voulme
    :type volume: str
    """
    runner = CliRunner()
    result = runner.invoke(volume_group, ["delete", volume, "--force"])
    assert (
        "Success: Volume test-volume deleted." in result.output.strip()
    ), "VOLUME DELETE TEST FAILED"
    print("VOLUME DELETE TEST OK")
