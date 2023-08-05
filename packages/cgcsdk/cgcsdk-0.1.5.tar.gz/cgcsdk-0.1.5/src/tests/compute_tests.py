import ast, time
from click.testing import CliRunner

# pylint: disable=import-error
from src.commands.compute.compute_cmd import compute_group

NAME = "test-pod"


def test_compute_list(volume="none"):
    """Module for testing compute list command

    :param volume: name of voulme, defaults to "none"
    :type volume: str, optional
    """
    runner = CliRunner()
    result = runner.invoke(compute_group, ["--debug", "list", "-d"])
    timeout = 0
    data = ast.literal_eval(result.output.strip())

    if volume != "none":
        while len(data) == 3 and timeout < 20:
            print(". ", end="", flush=True)
            time.sleep(3)
            timeout += 1
            result = runner.invoke(compute_group, ["--debug", "list", "-d"])
            data = ast.literal_eval(result.output.strip())
        print()

        assert (
            len(data) == 2
            and data[0][1] == "filebrowser"
            and data[0][3] == volume
            and data[1][0] == NAME
            and data[1][3] == volume
            and data[1][9] is not None
        ), f"COMPUTE LIST TEST FAILED: volume {volume}"
    else:
        while len(data) != 1 and timeout < 20:
            print(". ", end="", flush=True)
            time.sleep(3)
            timeout += 1
            result = runner.invoke(compute_group, ["--debug", "list", "-d"])
            try:
                data = ast.literal_eval(result.output.strip())
            except SyntaxError:
                print("COMPUTE LIST TEST FAILED: SyntaxError")
                return
        print()
        assert (
            len(data) == 1 and data[0][1] == "filebrowser" and data[0][3] is None
        ), f"COMPUTE LIST TEST FAILED: volume {volume}"

    print("COMPUTE LIST TEST OK")


def test_compute_create(volume):
    """Module for testing compute create command

    :param volume: name of voulme
    :type volume: str
    """
    runner = CliRunner()
    result = runner.invoke(
        compute_group,
        ["create", "tensorflow-jupyter", "--name", NAME, "--volume", "test-volume"],
    )
    assert (
        f"Success: tensorflow-jupyter Pod {NAME} has been created! Mounted volumes: {volume}"
        in result.output.strip()
    ), result.output.strip()
    print("COMPUTE CREATE TEST OK")


def test_compute_delete():
    """Module for testing compute delete command"""
    runner = CliRunner()
    result = runner.invoke(
        compute_group,
        ["delete", "--name", NAME],
    )
    assert (
        f"Success: Pod {NAME} successfully deleted with their service."
        in result.output.strip()
    ), "COMPUTE DELETE TEST FAILED"
    print("COMPUTE DELETE TEST OK")
