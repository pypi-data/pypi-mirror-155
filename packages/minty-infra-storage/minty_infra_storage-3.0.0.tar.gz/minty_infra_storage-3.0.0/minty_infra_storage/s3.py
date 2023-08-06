# SPDX-FileCopyrightText: Mintlab B.V.
#
# SPDX-License-Identifier: EUPL-1.2

import minio
import minio.credentials
import minty.infrastructure.mime_utils as mu
import os
import urllib.parse
from datetime import timedelta
from minty import Base
from minty.exceptions import ConfigurationConflict
from threading import BoundedSemaphore
from typing import BinaryIO, Optional
from uuid import UUID

max_concurrent_parsers = 1
mime_parser_semaphore = BoundedSemaphore(value=max_concurrent_parsers)


class S3Wrapper(Base):
    def __init__(self, filestore_config: list, base_directory: str):
        self.filestore_config = filestore_config
        self.base_directory = base_directory

    def _select_config(self, storage_location=None):
        """Select config from the stored configs."""
        if storage_location is None:
            return self.filestore_config[0]
        for config in self.filestore_config:
            if storage_location == config["name"]:
                return config

        raise ConfigurationConflict(
            f"No configuration found for '{storage_location}'"
        )

    def _generate_attachment_disposition(
        self, filename: Optional[str], download: bool
    ):
        """Generate the value of the Content-Disposition header

        https://developer.mozilla.org/en-US/docs/Web/HTTP/Headers/Content-Disposition
        """
        if download:
            content_disposition = "attachment"
        else:
            content_disposition = "inline"

        if filename is not None:
            encoded_filename = urllib.parse.quote(filename)
            content_disposition += f"; filename*=UTF-8''{encoded_filename}"

        return content_disposition

    def _s3_client(self, config) -> minio.Minio:
        """Build an AWS S3 client object from configuration"""

        minio_config = self._generate_minio_config(config)
        return minio.Minio(**minio_config)

    def _generate_minio_config(self, config):
        """Generate arguments to set up a Minio instance, using the configuration."""

        minio_parameters = {}

        access_key = config.get("access_id", None)
        secret_key = config.get("access_key", None)
        endpoint_url = config.get("endpoint_url", None)
        region_name = config.get("region_name", None)

        # If access id and key are not specified, Minio needs to be set up to use
        # will default to use the EC2 IAM role (which is what we want on
        # production)

        if all([access_key, secret_key]):
            minio_parameters["access_key"] = access_key
            minio_parameters["secret_key"] = secret_key
        else:
            minio_parameters[
                "credentials"
            ] = minio.credentials.IamAwsProvider()

        if endpoint_url is not None:
            if endpoint_url.startswith("https://"):
                minio_parameters["secure"] = True
                minio_parameters["endpoint"] = endpoint_url[len("https://") :]
            else:
                minio_parameters["secure"] = False
                minio_parameters["endpoint"] = endpoint_url[len("http://") :]

        if region_name is not None:
            minio_parameters["region"] = region_name

        return minio_parameters

    def _get_s3_bucket_and_key(self, config: dict, uuid: UUID) -> dict:
        """Generate `key` and `bucket` values for s3 based on the config type.

        :param config: config
        :type config: dict
        :param uuid: file_uuid
        :type uuid: UUID
        :return: dict
        :rtype: dict containing key and bucket values
        """
        if config["type"] == "s3":
            key = f"{self.base_directory}/{uuid}"
            try:
                bucket = config["bucket"]
            except KeyError as error:
                raise ConfigurationConflict(
                    "Invalid configuration for S3 found"
                ) from error
        elif config["type"] == "s3Legacy":
            key = str(uuid)
            bucket = self.base_directory
        else:
            raise ConfigurationConflict(
                "Invalid configuration for S3 found", "infra/s3/no_type"
            )
        return {"key": key, "bucket": bucket}

    def upload(
        self, file_handle: BinaryIO, uuid, file_size: Optional[int] = None
    ):
        """Uploads data from a file handle to S3"""

        if file_size is None:
            file_handle.seek(0, os.SEEK_END)
            file_size = file_handle.tell()
            file_handle.seek(0, os.SEEK_SET)

        timer = self.statsd.get_timer("filestorage_write_duration")
        with timer.time():
            config = self._select_config()

            location_name = config["name"]
            s3_config = self._get_s3_bucket_and_key(config=config, uuid=uuid)

            put_result = self._s3_client(config=config).put_object(
                bucket_name=s3_config["bucket"],
                object_name=s3_config["key"],
                data=file_handle,
                length=file_size,
            )
            etag = put_result.etag
        self.statsd.get_counter("filestorage_write_number").increment()

        global mime_parser_semaphore
        with mime_parser_semaphore:
            mimetype = mu.get_mime_type_from_handle(file_handle)

        return {
            "uuid": uuid,
            "md5": etag[1:-1],
            "size": file_size,
            "mime_type": mimetype,
            "storage_location": location_name,
        }

    def download_file(
        self, destination: BinaryIO, file_uuid, storage_location: str
    ):
        """Download a file from S3 to the file-handle `destination`

        :param destination: File handle to write the file's contents to
        :type destination: File
        :param file_uuid: UUID of the object to download
        :type file_uuid: UUID
        :param storage_location: Name of the storage configuration used to store
            this file.
        :type storage_location: str
        """

        config = self._select_config(storage_location)
        s3_config = self._get_s3_bucket_and_key(config=config, uuid=file_uuid)

        timer = self.statsd.get_timer("filestorage_read_duration")
        with timer.time():
            file_data = None
            try:
                file_data = self._s3_client(config=config).get_object(
                    bucket_name=s3_config["bucket"],
                    object_name=s3_config["key"],
                )
                for chunk in file_data.stream(128 * 1024):
                    destination.write(chunk)
            finally:
                if file_data:
                    file_data.close()
                    file_data.release_conn()

        destination.flush()
        self.statsd.get_counter("filestorage_read_number").increment()

        return

    def get_download_url(
        self,
        uuid,
        storage_location: str,
        filename: Optional[str],
        mime_type: str,
        download: bool,
    ):
        """Generate a pre-signed download url for given file uuid."""
        config = self._select_config(storage_location)
        s3_config = self._get_s3_bucket_and_key(config=config, uuid=uuid)

        presigned_url_expiration = config.get("presigned_url_expiration", 3600)
        cache_control = config.get("cache_control", "private, max-age=3600")

        content_disposition = self._generate_attachment_disposition(
            filename=filename, download=download
        )

        timer = self.statsd.get_timer(
            "filestore_generate_tmp_read_link_duration"
        )
        with timer.time():
            presigned_url = self._s3_client(
                config=config
            ).presigned_get_object(
                bucket_name=s3_config["bucket"],
                object_name=s3_config["key"],
                expires=timedelta(seconds=presigned_url_expiration),
                response_headers={
                    "response-content-disposition": content_disposition,
                    "response-content-type": mime_type,
                    "response-cache-control": cache_control,
                },
            )
        self.statsd.get_counter(
            "filestore_generate_tmp_read_link_number"
        ).increment()

        return presigned_url


class S3Infrastructure(Base):
    """Infrastructure Class for S3 Connection."""

    def __call__(self, config):
        """Create a new S3 connection using the specified configuration

        :param config: The configuration params necessary to connect to a S3 bucket.
        :return: A S3 handle for a bucket on a connection to an S3 server.
        :rtype: S3Wrapper
        """
        try:
            directory = config["storage_bucket"]
        except KeyError:
            try:
                directory = config["instance_uuid"]
            except KeyError as k:
                raise ConfigurationConflict(
                    "No instance UUID or storage bucket specified for S3 configuration"
                ) from k

        try:
            filestore_config = config["filestore"]
            if type(filestore_config) is not list:
                filestore_config = [filestore_config]
        except KeyError as error:
            raise ConfigurationConflict(
                "Invalid configuration for S3 found"
            ) from error

        return S3Wrapper(
            filestore_config=filestore_config, base_directory=directory
        )
