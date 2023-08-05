import click, requests, json, os, shutil, glob, base64, urllib, pkg_resources
from dotenv import load_dotenv


# pylint: disable=import-error
from src.utils.config_utils import get_config_path
from src.telemetry.basic import increment_metric
from src.utils.config_utils import add_to_config
from src.utils.config_utils import read_from_cfg
from src.utils.cryptography import rsa_crypto
from src.utils import prepare_headers
from src.utils.message_utils import prepare_error_message

env_file = pkg_resources.resource_filename("src", ".env")
load_dotenv(dotenv_path=env_file, verbose=True)

API_HOST = os.getenv("API_HOST")
API_PORT = os.getenv("API_PORT")
API_URL = f"http://{API_HOST}:{API_PORT}"
CGC_SECRET = os.getenv("CGC_SECRET")
TMP_DIR = os.path.join(get_config_path(), os.getenv("TMP_DIR"))


def get_jwt() -> str:
    """Command to get JWT token and api key for user

    :param username: _description_
    :type username: str
    :param password: _description_
    :type password: str
    """

    user_id = urllib.parse.quote(read_from_cfg("user_id"))
    passwd = urllib.parse.quote(read_from_cfg("passwd"))
    url = f"{API_URL}/v1/api/user/create/token"
    payload = f"grant_type=&username={user_id}&password={passwd}"

    jwt_headers = {
        "accept": "application/json",
        "Content-Type": "application/x-www-form-urlencoded",
    }
    try:
        res = requests.post(
            url,
            payload,
            headers=jwt_headers,
            timeout=10,
        )

        if res.status_code != 200:
            click.echo(f"JWT error: {res.status_code}, error: {res.text}")
            increment_metric("jwt.error")
            return None
        increment_metric("jwt.ok")

        data = json.loads(res.text)
        jwt = data["access_token"]
        return jwt

    except requests.exceptions.ReadTimeout:
        message = "Connection timed out. Try again or contact us at support@comtegra.pl"
        click.echo(prepare_error_message(message))


def auth_create_api_key():
    """Command to create API key and API secret for user and save it to config file."""
    url = f"{API_URL}/v1/api/user/create/api-key"
    headers = prepare_headers.prepare_headers_api_key()
    try:
        res = requests.post(
            url,
            headers=headers,
            timeout=10,
        )

        if res.status_code != 200:
            click.echo(f"error: {res.status_code}, error: {res.text}")
            increment_metric("api-key.error")
            return
        increment_metric("api-key.ok")

        data = json.loads(res.text)

        api_key = data["details"].get("_id")
        secret = data["details"].get("secret")

        add_to_config(api_key=api_key, api_secret=secret)

    except requests.exceptions.ReadTimeout:
        message = "Connection timed out. Try again or contact us at support@comtegra.pl"
        click.echo(prepare_error_message(message))


def save_and_unzip_file(res: requests.Response) -> str:
    """Command to save file, unzip it and return path to its directory.

    :param res: API response with file to save and unzip
    :type res: requests.Response
    :return: path to the directory containing the file
    :rtype: str
    """
    zip_file = res.headers.get("content-disposition").split('"')[1]

    if not os.path.isdir(TMP_DIR):
        os.makedirs(TMP_DIR)
    zip_file_path = f"{TMP_DIR}/{zip_file}"
    with open(zip_file_path, "wb") as f:
        f.write(res.content)

    unzip_dir = zip_file_path[:-4]
    shutil.unpack_archive(zip_file_path, unzip_dir)

    return unzip_dir


def get_aes_key_and_passwd(unzip_dir: str, priv_key_bytes: bytes):
    """Command to get AES key and password from the unzipped file.

    :param unzip_dir: path to the directory containing the file
    :type unzip_dir: str
    :param priv_key_bytes: private key bytes
    :type priv_key_bytes: bytes
    :return: AES key and password
    :rtype: str, str
    """
    encrypted_passwd_path = ""
    encrypted_aes_path = ""
    for file in glob.glob(
        f"{unzip_dir}/**/*encrypted*",
        recursive=True,
    ):
        if file.endswith("priv"):
            encrypted_aes_path = f"{file}"
        elif file.endswith("password"):
            encrypted_passwd_path = f"{file}"

    rsa_key = rsa_crypto.import_create_RSAKey(priv_key_bytes)

    with open(encrypted_aes_path, "rb") as aes, open(
        encrypted_passwd_path, "rb"
    ) as pwd:
        aes_key = rsa_crypto.decrypt_rsa(aes.read(), rsa_key).decode("ascii")
        passwd = base64.b64decode(rsa_crypto.decrypt_rsa(pwd.read(), rsa_key)).decode(
            "utf-8"
        )

    return aes_key, passwd
