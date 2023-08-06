#!/usr/bin/env python
#
# Copyright (c) 2022 Katonic Pty Ltd. All rights reserved.
#

from minio.credentials.providers import (
    AssumeRoleProvider,
    AWSConfigProvider,
    ChainedProvider,
    ClientGrantsProvider,
    EnvAWSProvider,
    EnvMinioProvider,
    IamAwsProvider,
    LdapIdentityProvider,
    MinioClientConfigProvider,
    Provider,
    StaticProvider,
    WebIdentityProvider
)