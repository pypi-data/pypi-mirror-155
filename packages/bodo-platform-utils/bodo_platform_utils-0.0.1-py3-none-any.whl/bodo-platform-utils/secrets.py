import boto3
import os
import json

workspace_uuid = os.environ.get("BODO_PLATFORM_WORKSPACE_UUID")
aws_region = os.environ.get("BODO_PLATFORM_WORKSPACE_REGION")


# Made this function as private and won't be accessible directly
def _get_ssm_parameters(parameter_name):
    ssm_client = boto3.client("ssm", aws_region)
    parameters = ssm_client.get_parameter(Name=parameter_name, WithDecryption=True)
    return json.loads(parameters["Parameter"].get("Value"))


# Users have to use the below helper functions to get the secrets from SSM.
def snowflake_credentials():
    parameter_name = '/bodo/workspaces/{}/secrets/snowflake_credentials'.format(workspace_uuid)
    return _get_ssm_parameters(parameter_name)


def workspace_data():
    parameter_name = '/bodo/workspaces/{}/data'.format(workspace_uuid)
    return _get_ssm_parameters(parameter_name)