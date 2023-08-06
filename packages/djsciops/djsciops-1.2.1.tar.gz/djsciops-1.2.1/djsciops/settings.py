import appdirs
import pathlib
import os
import yaml
from packaging import version as semantic_version
from . import __version__ as version

CONFIG_TEMPLATE = """
version: "{djsciops_version}"
aws:
  account_id: "{djsciops_aws_account_id}"
s3:
  role: "{djsciops_s3_role}"
  bucket: "{djsciops_s3_bucket}"
djauth:
  client_id: "{djsciops_djauth_client_id}"
boto3:
  multipart_threshold: {multipart_threshold}
  max_concurrency: {max_concurrency}
  multipart_chunksize: {multipart_chunksize}
  use_threads: {use_threads}
"""

LOG_LEVEL = os.getenv("DJSCIOPS_LOG_LEVEL", "info")

DEFAULT_THRESHOLD = 1024 * 25
DEFAULT_CONCURRENCY = 10
DEFAULT_CHUNKSIZE = 1024 * 25
DEFAULT_THREAD_USE = True


def get_config(stdin_enabled=True):
    from .log import log

    config_directory = appdirs.user_data_dir(appauthor="datajoint", appname="djsciops")
    try:
        # loading existing config
        config = load_config(pathlib.Path(config_directory, "config.yaml").read_text())
        log.info(
            "Existing configuration detected. Loading from "
            f"{pathlib.Path(config_directory, 'config.yaml')}..."
        )
        # update djsciops config for boto3 transfer config addition
        if semantic_version.parse(config["version"]) < semantic_version.parse("1.2.0"):
            config["boto3"] = dict(
                multipart_threshold=DEFAULT_THRESHOLD,
                max_concurrency=DEFAULT_CONCURRENCY,
                multipart_chunksize=DEFAULT_CHUNKSIZE,
                use_threads=DEFAULT_THREAD_USE,
            )
            config["version"] = version
            save_config(yaml.dump(config), config_directory)
        return config
    except FileNotFoundError as e:
        if not stdin_enabled:
            config = dict(
                version=version,
                aws=dict(account_id=""),
                s3=dict(role="", bucket=""),
                djauth=dict(client_id=""),
                boto3=dict(
                    multipart_threshold=DEFAULT_THRESHOLD,
                    max_concurrency=DEFAULT_CONCURRENCY,
                    multipart_chunksize=DEFAULT_CHUNKSIZE,
                    use_threads=DEFAULT_THREAD_USE,
                ),
            )
            log.warning("No config provided. Generating empty config.")
            return config
        log.info(
            "Welcome! We've detected that this is your first time using DataJoint "
            "SciOps CLI tools. We'll need to ask a few questions to initialize properly."
        )
        # generate default config
        config = CONFIG_TEMPLATE.format(
            djsciops_aws_account_id=(
                os.getenv("DJSCIOPS_AWS_ACCOUNT_ID")
                if os.getenv("DJSCIOPS_AWS_ACCOUNT_ID")
                else input("\n   -> AWS Account ID? ")
            ),
            djsciops_s3_role=(
                os.getenv("DJSCIOPS_S3_ROLE")
                if os.getenv("DJSCIOPS_S3_ROLE")
                else input("\n   -> S3 Role? ")
            ),
            djsciops_s3_bucket=(
                os.getenv("DJSCIOPS_S3_BUCKET")
                if os.getenv("DJSCIOPS_S3_BUCKET")
                else input("\n   -> S3 Bucket? ")
            ),
            djsciops_djauth_client_id=(
                os.getenv("DJSCIOPS_DJAUTH_CLIENT_ID")
                if os.getenv("DJSCIOPS_DJAUTH_CLIENT_ID")
                else input("\n   -> DataJoint Account Client ID? ")
            ),
            multipart_threshold=DEFAULT_THRESHOLD,
            max_concurrency=DEFAULT_CONCURRENCY,
            multipart_chunksize=DEFAULT_CHUNKSIZE,
            use_threads=DEFAULT_THREAD_USE,
            djsciops_version=version,
            djsciops_log_level=os.getenv("DJSCIOPS_LOG_LEVEL", "info"),
        )
        # write config
        save_config(config, config_directory)

        log.info(
            "Thank you! We've saved your responses to "
            f"{pathlib.Path(config_directory, 'config.yaml')} so you won't need to "
            "specify this again."
        )
        # return config
        return load_config(config)


def load_config(config_str):
    from .log import log

    config = yaml.safe_load(config_str)
    if not config["aws"]["account_id"]:
        log.warning("Missing `aws.account_id` configuration")
    if not config["s3"]["role"]:
        log.warning("Missing `s3.role` configuration")
    if not config["s3"]["bucket"]:
        log.warning("Missing `s3.bucket` configuration")
    if not config["djauth"]["client_id"]:
        log.warning("Missing `djauth.client_id` configuration")
    return config


def save_config(config, config_directory):
    os.makedirs(config_directory, exist_ok=True)
    with open(pathlib.Path(config_directory, "config.yaml"), "w") as f:
        f.write(config)
