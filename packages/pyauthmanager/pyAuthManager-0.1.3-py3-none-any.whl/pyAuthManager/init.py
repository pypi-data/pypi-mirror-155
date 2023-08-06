import os
import pyAuthManager.aws as aws
import pyAuthManager.gcp as gcp
import pyAuthManager.azure as azure


def __init_aws():
    """
    Init AWS Credentials based on expecting environment variables
    Parameters
    ----------
    None

    Returns
    -------
    Nothing
    """

    params = {}
    params['region'] = os.environ.get('AWS_REGION')
    params['userpool'] = os.environ.get('AWS_USER_POOL_ID')
    params['id'] = os.environ.get('AWS_CLIENT_ID')
    params['secret'] = os.environ.get('AWS_CLIENT_SECRET')

    aws.set_credentials(params)


def __init_gcp():
    """
    Init GCP Credentials based on expecting environment variables
    Parameters
    ----------
    None

    Returns
    -------
    Nothing
    """

    params = {}
    params['api_key'] = os.environ.get('GCP_API_KEY')
    params['service_account_key'] = os.environ.get('GCP_SERVICE_ACCOUNT_KEY')
    params['account_type'] = os.environ.get('GCP_ACCOUNT_TYPE')
    params['project_id'] = os.environ.get('GCP_PROJECT_ID')
    params['private_key_id'] = os.environ.get('GCP_PRIVATE_KEY_ID')
    params['private_key'] = os.environ.get('GCP_PRIVATE_KEY')
    params['client_email'] = os.environ.get('GCP_CLIENT_EMAIL')
    params['client_id'] = os.environ.get('GCP_CLIENT_ID')
    params['auth_uri'] = os.environ.get('GCP_AUTH_URI')
    params['token_uri'] = os.environ.get('GCP_TOKEN_URI')
    params['auth_provider_x509_cert_url'] = os.environ.get('GCP_AUTH_PROVIDER_X509_CERT_URL')
    params['client_x509_cert_url'] = os.environ.get('GCP_CLIENT_X509_CERT_URL')

    gcp.set_credentials(params)


def __init_azure():
    """
    Init Azure Credentials based on expecting environment variables
    Parameters
    ----------
    None

    Returns
    -------
    Nothing
    """

    params = {}
