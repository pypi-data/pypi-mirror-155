#!/usr/bin/env python
#
# Copyright (c) 2022 Katonic Pty Ltd. All rights reserved.
#

from minio.signer import (
    presign_v4,
    sign_v4_s3,
    sign_v4_sts,
    get_credential_string,
    post_presign_v4
)