#!/usr/bin/env python
#
# Copyright (c) 2022 Katonic Pty Ltd. All rights reserved.
#

from minio import Minio

from katonic.filemanager.progress import Progress


class Filemanager:
    """
    Simple Storage Service client to perform bucket and object
    operations for the Katonic File Manager.

    Args:
        access_key: Access key  of your File Manager inside your Katonic service account.
        secret_key: Secret Key of your File Manager inside your Katonic service account.

    Return: 
        :class:`filemanager <Filemanger>` object

    Example::

        # Create client with access and secret key.
        client = Filemanager("s3.amazonaws.com", "ACCESS-KEY", "SECRET-KEY")
        # Create client with access key and secret key with specific region.
        client = Filemanager(
            access_key="Q3AM3UQ867SPQQA43P2F",
            secret_key="zuf+tfteSlswRu7BJ86wekitnifILbZam1KYY3TG",
        )
    """
    def __init__(
        self,
        access_key=None,
        secret_key=None,
    ):
        if access_key and secret_key:
            self._fm = Minio(
                endpoint="minio-server.default.svc.cluster.local:9000",
                access_key=access_key,
                secret_key=secret_key,
                secure=False,
            )
        else:
            raise ValueError("Please provide the Access Key and Secret Key in order to Initialize the session.")

    def client(
        self
    ):
        """Return a File Manager Client"""
        return self._fm

    def put_file_object(
        self,
        bucket_name,
        object_name,
        file_path,
        content_type="application/octet-stream",
        metadata=None,
        sse=None,
        part_size=0,
        num_parallel_uploads=3,
        tags=None,
        retention=None,
        legal_hold=False,
    ):
        """
        Uploads data from a file to an object in a bucket.

        Args:
            bucket_name: Name of the bucket.
            object_name: Object name in the bucket.
            file_path: Name of file to upload.
            content_type: Content type of the object.
            metadata: Any additional metadata to be uploaded along
                with your PUT request.
            sse: Server-side encryption.
            progress: A progress object
            part_size: Multipart part size
            num_parallel_uploads: Number of parallel uploads.
            tags: :class:`Tags` for the object.
            retention: :class:`Retention` configuration object.
            legal_hold: Flag to set legal hold for the object.

        Return:
            :class:`ObjectWriteResult` object.

        Example::

            # Upload data.
            result = client.put_file_object(
                "my-bucket", "my-object", "my-filename",
            )
            # Upload data with metadata.
            result = client.put_file_object(
                "my-bucket", "my-object", "my-filename",
                metadata={"My-Project": "one"},
            )
            # Upload data with tags, retention and legal-hold.
            date = datetime.utcnow().replace(
                hour=0, minute=0, second=0, microsecond=0,
            ) + timedelta(days=30)
            tags = Tags(for_object=True)
            tags["User"] = "jsmith"
            result = client.put_file_object(
                "my-bucket", "my-object", "my-filename",
                tags=tags,
                retention=Retention(GOVERNANCE, date),
                legal_hold=True,
            )
        """
        return self._fm.fput_object(
                bucket_name,
                object_name,
                file_path,
                content_type=content_type,
                metadata=metadata,
                sse=sse,
                progress=Progress(),
                part_size=part_size,
                num_parallel_uploads=num_parallel_uploads,
                tags=tags,
                retention=retention,
                legal_hold=legal_hold,
            )

    def put_byte_object(
        self,
        bucket_name,
        object_name,
        data,
        length,
        content_type="application/octet-stream",
        metadata=None,
        sse=None,
        part_size=0,
        num_parallel_uploads=3,
        tags=None,
        retention=None,
        legal_hold=False,
    ):
        """
        Uploads data from a stream to an object in a bucket.

        Args:
            bucket_name: Name of the bucket.
            object_name: Object name in the bucket.
            data: An object having callable read() returning bytes object.
            length: Data size; -1 for unknown size and set valid part_size.
            content_type: Content type of the object.
            metadata: Any additional metadata to be uploaded along
                with your PUT request.
            sse: Server-side encryption.
            progress: A progress object;
            part_size: Multipart part size.
            num_parallel_uploads: Number of parallel uploads.
            tags: :class:`Tags` for the object.
            retention: :class:`Retention` configuration object.
            legal_hold: Flag to set legal hold for the object.

        Return:
            :class:`ObjectWriteResult` object.

        Example::

            # Upload data.
            result = client.put_byte_object(
                "my-bucket", "my-object", io.BytesIO(b"hello"), 5,
            )
            # Upload data with metadata.
            result = client.put_byte_object(
                "my-bucket", "my-object", io.BytesIO(b"hello"), 5,
                metadata={"My-Project": "one"},
            )
            # Upload data with tags, retention and legal-hold.
            date = datetime.utcnow().replace(
                hour=0, minute=0, second=0, microsecond=0,
            ) + timedelta(days=30)
            tags = Tags(for_object=True)
            tags["User"] = "jsmith"
            result = client.put_byte_object(
                "my-bucket", "my-object", io.BytesIO(b"hello"), 5,
                tags=tags,
                retention=Retention(GOVERNANCE, date),
                legal_hold=True,
            )
        """
        return self._fm.put_object(
                bucket_name,
                object_name,
                data,
                length,
                content_type=content_type,
                metadata=metadata,
                sse=sse,
                progress=Progress(),
                part_size=part_size,
                num_parallel_uploads=num_parallel_uploads,
                tags=tags,
                retention=retention,
                legal_hold=legal_hold,
            )