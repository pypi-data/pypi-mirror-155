from colorama import Fore, Style


def prepare_error_message(message: str) -> str:
    """Prepare error message for CLI.

    :param message: error message.
    :type message: str
    """
    return f"{Fore.RED}Error: {message}{Style.RESET_ALL}"


def prepare_warning_message(message: str) -> str:
    """Prepare warning message for CLI.

    :param message: warning message.
    :type message: str
    """
    return f"{Fore.YELLOW}Warning: {message}{Style.RESET_ALL}"


def prepare_success_message(message: str) -> str:
    """Prepare success message for CLI.

    :param message: success message.
    :type message: str
    """
    return f"{Fore.GREEN}Success: {message}{Style.RESET_ALL}"
