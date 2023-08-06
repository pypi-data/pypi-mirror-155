#!/usr/bin/env python
#
# Copyright (c) 2022 Katonic Pty Ltd. All rights reserved.
#

from minio.datatypes import (
    Bucket,
    CompleteMultipartUploadResult,
    EventIterable,
    ListAllMyBucketsResult,
    ListMultipartUploadsResult,
    ListPartsResult,
    Object,
    Part,
    Upload,
    PostPolicy,
    parse_copy_object,
    parse_list_objects
)