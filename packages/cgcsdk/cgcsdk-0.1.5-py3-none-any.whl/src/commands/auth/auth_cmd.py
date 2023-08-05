import click, requests, os, shutil, pkg_resources
from dotenv import load_dotenv


# pylint: disable=import-error
from src.utils.config_utils import get_config_path
from src.commands.auth import auth_utils
from src.utils.cryptography import rsa_crypto
from src.utils.config_utils import add_to_config
from src.utils.prepare_headers import get_api_url_and_prepare_headers_register
from src.telemetry.basic import increment_metric
from src.utils.message_utils import prepare_error_message

env_file = pkg_resources.resource_filename("src", ".env")
load_dotenv(dotenv_path=env_file, verbose=True)

TMP_DIR = os.path.join(get_config_path(), os.getenv("TMP_DIR"))


@click.command("register")
@click.option("--user_id", "-u", "user_id", prompt=True)
@click.option("--access_key", "-k", "access_key", prompt=True)
def auth_register(user_id: str, access_key: str):
    """Register a user in system using user id and access key.

    :param user_id: username received in invite
    :type user_id: str
    :param access_key: access key received in invite
    :type access_key: str
    """

    url, headers = get_api_url_and_prepare_headers_register(user_id, access_key)
    pub_key_bytes, priv_key_bytes = rsa_crypto.key_generate_pair()
    payload = pub_key_bytes

    try:
        res = requests.post(
            url,
            data=payload,
            headers=headers,
            allow_redirects=True,
            timeout=10,
        )

        if res.status_code != 200:
            increment_metric("register.error")
            if res.status_code == 401:
                click.echo("Could not validate user id or access key")
                return

            click.echo(f"{res.status_code}, {res.text}")
            return

        increment_metric("register.ok")

        unzip_dir = auth_utils.save_and_unzip_file(res)
        aes_key, passwd = auth_utils.get_aes_key_and_passwd(unzip_dir, priv_key_bytes)

        add_to_config(user_id=user_id, passwd=passwd, aes_key=aes_key)
        auth_utils.auth_create_api_key()

        click.echo("Register successful!")
        shutil.rmtree(TMP_DIR)
    except requests.exceptions.ReadTimeout:
        message = "Connection timed out. Try again or contact us at support@comtegra.pl"
        click.echo(prepare_error_message(message))
