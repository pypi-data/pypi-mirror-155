import boto3
from config import WORKSPACE_UUID, REGION, CLOUD_PROVIDER
import json
from utils_types import CloudProvider
from mpi4py import MPI


def _get_ssm_parameter(parameter_name):
    ssm_client = boto3.client("ssm", REGION)
    parameters = ssm_client.get_parameter(Name=parameter_name, WithDecryption=True)
    data = json.loads(parameters["Parameter"].get("Value"))
    return data


# Made this function as private and won't be accessible directly
def _get_ssm_parameter_parallel(parameter_name):
    comm = MPI.COMM_WORLD
    data_or_e = None
    if comm.Get_rank() == 0:
        try:
            data_or_e = _get_ssm_parameter(parameter_name)
        except Exception as e:
            data_or_e = e

    data_or_e = comm.bcast(data_or_e)

    if isinstance(data_or_e, Exception):
        raise data_or_e
    data = data_or_e
    return data


# Users have to use the below helper functions to get the secrets from SSM.
def snowflake_credentials(_parallel=True):
    if CLOUD_PROVIDER == CloudProvider.AWS:
        parameter_name = (
            f"/bodo/workspaces/{WORKSPACE_UUID}/secrets/snowflake_credentials"
        )
        if _parallel:
            return _get_ssm_parameter_parallel(parameter_name)
        else:
            return _get_ssm_parameter(parameter_name)
    elif CLOUD_PROVIDER == CloudProvider.AZURE:
        raise NotImplementedError("This functionality is not supported for Azure.")
    else:
        raise ValueError(f"Unrecognized Cloud Provider: {CLOUD_PROVIDER}")