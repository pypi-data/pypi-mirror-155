import pathlib
import os
import boto3.s3.transfer
import tqdm
from typing import Union
from . import utils as djsciops_utils
from djsciops import settings as djsciops_settings
import collections.abc
import logging
from .log import log, TqdmToLogger


def _generate_upload_mapping(
    session,
    s3_bucket: str,
    source: Union[str, list],
    destination: Union[str, list],
) -> tuple:
    if (
        isinstance(source, list)
        and isinstance(destination, list)
        and len(source) == len(destination)
    ):
        log.info("Upload mapping provided.")
        # expect file_paths to be list of Path, object_paths to be list of PurePosixPath
        file_paths, object_paths = (source, destination)
        existing_objects = {
            pathlib.PurePosixPath(op.key)
            for op in session.s3.Bucket(s3_bucket).objects.filter(
                Prefix=os.path.commonprefix(object_paths)
            )
        }
        file_paths, object_paths = tuple(
            zip(
                *(
                    (fp, op)
                    for fp, op in zip(file_paths, object_paths)
                    if op not in existing_objects
                )
            )
        )
        assert file_paths, "All files already exist in object store."
    else:
        # modes: file -> directory, directory -> directory
        assert destination[-1] == "/", "Must point to a directory in object store."
        source = pathlib.Path(source).resolve()
        # recursively list files that are not hidden or directories
        file_paths = {
            fp.relative_to(source)
            for fp in source.rglob("*")
            if not fp.is_dir() and not str(fp.name).startswith(".")
        }
        file_paths = (
            {pathlib.PurePosixPath(_) for _ in file_paths}
            if file_paths
            else {pathlib.PurePosixPath(source.name)}
        )  # if specified a single file
        # recursively list objects
        existing_objects = {
            pathlib.PurePosixPath(op.key.replace(destination, ""))
            for op in session.s3.Bucket(s3_bucket).objects.filter(Prefix=destination)
        }
        # exclude objects that exist and verify that new objects are present
        file_paths = file_paths - existing_objects
        assert file_paths, "All files already exist in object store."
        object_paths = [pathlib.PurePosixPath(destination, fp) for fp in file_paths]
        file_paths = [
            pathlib.Path(source if source.is_dir() else source.parent, fp)
            for fp in file_paths
        ]

    return file_paths, object_paths


def _generate_download_mapping(
    session,
    s3_bucket: str,
    source: Union[str, list],
    destination: Union[str, list],
) -> tuple:
    if (
        isinstance(source, list)
        and isinstance(destination, list)
        and len(source) == len(destination)
    ):
        log.error("List download not implemented")
    else:
        # modes: file -> directory, directory -> directory
        assert destination[-1] == (
            "/" if os.name == "posix" else "\\"
        ), "Must point to a local directory"
        destination = pathlib.Path(destination).resolve()
        log.debug(f"destination: {destination}")
        # recursively list objects
        object_root = s.parent if (s := pathlib.PurePosixPath(source)).suffix else s
        object_paths = {
            pathlib.PurePosixPath(op.key).relative_to(object_root)
            for op in session.s3.Bucket(s3_bucket).objects.filter(Prefix=source)
        }
        log.debug(f"object_paths: {object_paths}")
        # recursively list files that are not hidden or directories
        existing_objects = {
            fp.relative_to(destination)
            for fp in destination.rglob("*")
            if not fp.is_dir() and not str(fp.name).startswith(".")
        }
        log.debug(f"existing_objects: {existing_objects}")
        existing_objects = (
            {pathlib.PurePosixPath(_) for _ in existing_objects}
            if existing_objects
            else {pathlib.PurePosixPath(destination.name)}
        )  # if specified a single file
        # exclude objects that exist and verify that new objects are present
        object_paths = object_paths - existing_objects
        assert object_paths, "All files already exist locally."
        file_paths = [pathlib.Path(destination, op) for op in object_paths]
        log.debug(f"file_paths: {file_paths}")
        object_paths = [pathlib.PurePosixPath(object_root, op) for op in object_paths]

    return object_paths, file_paths


def list_files(
    session,
    s3_bucket: str,
    s3_prefix: str,
):
    objects = [
        dict(key=op.key, _size=op.size)
        for op in session.s3.Bucket(s3_bucket).objects.filter(Prefix=s3_prefix)
    ]
    objects = sorted(objects, key=lambda o: o["key"])

    tree = {}
    for o in objects:
        node = tree  # local node
        levels = o["key"].split("/")
        for level in levels:
            node = node.setdefault(level, dict())
            node["_size"] = (
                o["_size"] + node["_size"] if "_size" in node else o["_size"]
            )

    def update(d):
        for k, v in d.items():
            if isinstance(v, collections.abc.Mapping) and len(v) > 1:
                if k != "_size":
                    size = d[k].pop("_size")
                    d[k] = update(d.get(k, {}))
            else:
                d[k] = None
        return d

    return update(tree)


def upload_files(
    session,
    s3_bucket: str,
    source: Union[str, list],
    destination: Union[str, list],
):
    file_paths, object_paths = _generate_upload_mapping(
        session=session,
        s3_bucket=s3_bucket,
        source=source,
        destination=destination,
    )
    log.info("Starting upload")
    with tqdm.tqdm(
        total=sum(os.stat(fp).st_size for fp in file_paths),
        unit="B",
        unit_scale=True,
        desc="",
        file=TqdmToLogger(log, level=logging.INFO),
    ) as pbar:
        for fp, op in zip(file_paths, object_paths):
            log.info(f"{fp}->{op}")
            ## hash metadata
            contents_hash = djsciops_utils.uuid_from_file(fp)
            log.debug(f"contents_hash.hex: {contents_hash.hex}")
            ## upload
            boto3_config = djsciops_settings.get_config()["boto3"]
            session.s3.Bucket(s3_bucket).upload_file(
                Filename=str(fp),
                Key=str(op),
                Config=boto3.s3.transfer.TransferConfig(
                    multipart_threshold=boto3_config["multipart_threshold"],
                    max_concurrency=boto3_config["max_concurrency"],
                    multipart_chunksize=boto3_config["multipart_chunksize"],
                    use_threads=boto3_config["use_threads"],
                ),
                Callback=lambda bytes_transferred: pbar.update(bytes_transferred),
                ExtraArgs={"Metadata": {"contents_hash": contents_hash.hex}},
            )


def download_files(
    session,
    s3_bucket: str,
    source: Union[str, list],
    destination: Union[str, list],
):
    object_paths, file_paths = _generate_download_mapping(
        session=session,
        s3_bucket=s3_bucket,
        source=source,
        destination=destination,
    )
    log.info("Starting download")
    with tqdm.tqdm(
        total=sum(
            session.s3.Object(s3_bucket, str(op)).content_length for op in object_paths
        ),
        unit="B",
        unit_scale=True,
        desc="",
        file=TqdmToLogger(log, level=logging.INFO),
    ) as pbar:
        for op, fp in zip(object_paths, file_paths):
            log.info(f"{op}->{fp}")
            # check if dir exists
            if not os.path.exists(os.path.dirname(fp)):
                os.makedirs(os.path.dirname(fp))
            ## download
            boto3_config = djsciops_settings.get_config()["boto3"]
            session.s3.Bucket(s3_bucket).download_file(
                Key=str(op),
                Filename=str(fp),
                Config=boto3.s3.transfer.TransferConfig(
                    multipart_threshold=boto3_config["multipart_threshold"],
                    max_concurrency=boto3_config["max_concurrency"],
                    multipart_chunksize=boto3_config["multipart_chunksize"],
                    use_threads=boto3_config["use_threads"],
                ),
                Callback=lambda bytes_transferred: pbar.update(bytes_transferred),
            )
