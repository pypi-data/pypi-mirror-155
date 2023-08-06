#!/usr/bin/env python
#
# Copyright (c) 2022 Katonic Pty Ltd. All rights reserved.
#

from minio.lifecycleconfig import (
    LifecycleConfig,
    Transition,
    NoncurrentVersionTransition,
    NoncurrentVersionExpiration,
    Expiration,
    AbortIncompleteMultipartUpload,
    Rule
)