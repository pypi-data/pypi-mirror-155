import os
from utils_types import CloudProvider

WORKSPACE_UUID = os.environ.get("BODO_PLATFORM_WORKSPACE_UUID")
REGION = os.environ.get("BODO_PLATFORM_WORKSPACE_REGION")

# Default to AWS for now.
CLOUD_PROVIDER = CloudProvider(
    os.environ.get("BODO_PLATFORM_WORKSPACE_CLOUD_PROVIDER", "AWS")
)
