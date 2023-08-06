import argparse
import sys
import yaml
from djsciops import __version__ as version
from djsciops import authentication as djsciops_authentication
from djsciops import axon as djsciops_axon
from djsciops import settings as djsciops_settings


def djsciops(args: list = None):
    """
    Primary console interface for djsciops's shell utilities.

    :param args: List of arguments to be passed in, defaults to reading stdin
    :type args: list, optional
    """
    from djsciops.log import log

    parser = argparse.ArgumentParser(
        prog="djsciops", description="DataJoint SciOps console interface."
    )
    parser.add_argument(
        "-V", "--version", action="version", version=f"djsciops {version}"
    )
    command = parser.add_subparsers(dest="command")

    axon = command.add_parser("axon", description="Manage object store data.")
    axon_subcommand = axon.add_subparsers(dest="subcommand")

    axon_upload = axon_subcommand.add_parser(
        "upload", description="Copy objects by uploading to object store."
    )
    axon_upload_required_named = axon_upload.add_argument_group(
        "required named arguments"
    )
    axon_upload_required_named.add_argument(
        "source",
        type=str,
        help="Source file or directory on client.",
    )
    axon_upload_required_named.add_argument(
        "destination",
        type=str,
        help="Target directory in object store.",
    )

    axon_download = axon_subcommand.add_parser(
        "download", description="Download objects from object store."
    )
    axon_download_required_named = axon_download.add_argument_group(
        "required named arguments"
    )
    axon_download_required_named.add_argument(
        "source",
        type=str,
        help="Source file or directory in object store.",
    )
    axon_download_required_named.add_argument(
        "destination",
        type=str,
        help="Target directory on client.",
    )

    config = command.add_parser("config", description="View or modify djsciops config")

    config_optional_named = config.add_argument_group("optional named arguments")
    config_optional_named.add_argument(
        "key", type=str, nargs="?", default=None, help="Configuration key."
    )
    config_optional_named.add_argument(
        "value", type=str, nargs="?", default=None, help="New configuration value."
    )

    kwargs = vars(parser.parse_args(args if sys.argv[1:] else ["-h"]))
    config = djsciops_settings.get_config()
    if kwargs["command"] == "axon":
        if kwargs["subcommand"] == "upload":
            djsciops_axon.upload_files(
                session=djsciops_authentication.Session(
                    aws_account_id=config["aws"]["account_id"],
                    s3_role=config["s3"]["role"],
                    auth_client_id=config["djauth"]["client_id"],
                ),
                s3_bucket=config["s3"]["bucket"],
                source=kwargs["source"],
                destination=kwargs["destination"],
            )
        elif kwargs["subcommand"] == "download":
            djsciops_axon.download_files(
                session=djsciops_authentication.Session(
                    aws_account_id=config["aws"]["account_id"],
                    s3_role=config["s3"]["role"],
                    auth_client_id=config["djauth"]["client_id"],
                ),
                s3_bucket=config["s3"]["bucket"],
                source=kwargs["source"],
                destination=kwargs["destination"],
            )
    elif kwargs["command"] == "config":

        def _recursive_index(key, config_obj, mode="get"):
            if "." not in key:
                if mode == "get":
                    return config_obj[key]
                elif mode == "set":
                    return key, config_obj
            config_keys = key.split(".")
            return _recursive_index(
                ".".join(config_keys[1:]), config_obj[config_keys[0]], mode=mode
            )

        def _cast_input(s, key):
            if s.lower() == "true":
                return True
            elif s.lower() == "false":
                return False
            elif not s.isnumeric() or key == "aws.account_id":
                return s
            else:
                try:
                    return int(s)
                except ValueError:
                    return float(s)

        if kwargs["key"] and not kwargs["value"]:
            log.info(
                yaml.dump(_recursive_index(kwargs["key"], config)),
                extra={"disable_format": True},
            )

        elif kwargs["key"] and kwargs["value"]:
            curr_key, curr_object = _recursive_index(kwargs["key"], config, mode="set")
            curr_object[curr_key] = _cast_input(kwargs["value"], kwargs["key"])
            config_directory = djsciops_settings.appdirs.user_data_dir(
                appauthor="datajoint", appname="djsciops"
            )
            djsciops_settings.save_config(yaml.dump(config), config_directory)

        else:
            log.info(yaml.dump(config), extra={"disable_format": True})
    raise SystemExit


if __name__ == "__main__":
    djsciops()
