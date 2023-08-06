
import boto3
import botocore.exceptions

import json
import urllib.request


class AWSConfig:
    pass


aws_config = AWSConfig()
aws_config.keys = None
aws_config.region = ""
aws_config.user_pool_id = ""
aws_config.client_id = ""
aws_config.client_secret = ""
aws_config.client = None


def set_credentials(params={}):
    """
    Use to set the AWS credentials needed
    Parameters
    ----------
    params  (dict) : AWS parameters

    Returns
    -------
    Nothing
    """

    # Instruction meaning
    # If all values are not None, nones would be set to False, else True
    nones = not all(params.values())

    if nones is True:
        raise Exception(
            "Some environment variables are missing ... Cannot continue !")

    if aws_config.client is None:
        aws_config.client = boto3.client('cognito-idp')

    aws_config.region = params.get('region', '')
    aws_config.user_pool_id = params.get('userpool', '')
    aws_config.client_id = params.get('id', '')
    aws_config.client_secret = params.get('secret', '')

    keys_url = 'https://cognito-idp.{}.amazonaws.com/{}/.well-known/jwks.json'.format(
        aws_config.region, aws_config.user_pool_id)

    try:
        with urllib.request.urlopen(keys_url) as f:
            response = f.read()
        aws_config.keys = json.loads(response.decode('utf-8'))['keys']
    except Exception as e:
        aws_config.keys = None
