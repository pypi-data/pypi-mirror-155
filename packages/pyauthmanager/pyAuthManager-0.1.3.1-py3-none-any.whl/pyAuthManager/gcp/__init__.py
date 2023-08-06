
import firebase_admin
from firebase_admin import credentials

import pyAuthManager.libs.response as resp

VERIFY_EMAIL = 'VERIFY_EMAIL'


class GCPConfig:
    pass


gcp_config = GCPConfig()
gcp_config.service_account = ""
gcp_config.app = None
gcp_config.api_key = ""
gcp_config.service_account_key = ""
gcp_config.gcip_rest_urls = {}


def set_credentials(params={}):
    """
    Use to set the GCP credentials needed
    Parameters
    ----------
    params  (dict) : GCP parameters

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

    gcp_config.api_key = params.get('api_key', '')
    
    if gcp_config.api_key == '' :
        raise Exception(
            "Configuration is not valid. The app could not be initialize ... Cannot continue !")
            
    gcp_config.gcip_rest_urls = {
        'refresh_token': {'url': 'https://securetoken.googleapis.com/v1/token'},
        'signup': {'url': 'https://identitytoolkit.googleapis.com/v1/accounts:signUp'},
        'signin_with_pwd': {'url': 'https://identitytoolkit.googleapis.com/v1/accounts:signInWithPassword'},
        'signin_anonym': {'url': 'https://identitytoolkit.googleapis.com/v1/accounts:signUp'},
        'signin_with_oauth': {'url': 'https://identitytoolkit.googleapis.com/v1/accounts:signInWithIdp'},
        'fetch_provider': {'url': 'https://identitytoolkit.googleapis.com/v1/accounts:createAuthUri'},
        'send_pwd_reset_mail': {
            'url': 'https://identitytoolkit.googleapis.com/v1/accounts:sendOobCode',
            'request_type': 'PASSWORD_RESET',
        },
        'verify_pwd_reset_code': {'url': 'https://identitytoolkit.googleapis.com/v1/accounts:resetPassword'},
        'confirm_pwd_reset': {'url': 'https://identitytoolkit.googleapis.com/v1/accounts:resetPassword'},
        'change_email': {'url': 'https://identitytoolkit.googleapis.com/v1/accounts:update'},
        'change_pwd': {'url': 'https://identitytoolkit.googleapis.com/v1/accounts:update'},
        'update_profile': {'url': 'https://identitytoolkit.googleapis.com/v1/accounts:update'},
        'get_user_data': {'url': 'https://identitytoolkit.googleapis.com/v1/accounts:lookup'},
        'send_verify_mail': {
            'url': 'https://identitytoolkit.googleapis.com/v1/accounts:sendOobCode',
            'request_type': 'VERIFY_EMAIL',
        },
        'confirm_mail_verification': {'url': 'https://identitytoolkit.googleapis.com/v1/accounts:update'},
    }
            
    gcp_config.service_account_key = params.get('service_account_key', None)
    
    if gcp_config.service_account_key is None :
        raise Exception(
            "Configuration is not valid. The app could not be initialize ... Cannot continue !")

    if gcp_config.app is None:
        cred = credentials.Certificate(gcp_config.service_account_key)
        gcp_config.app = firebase_admin.initialize_app(cred)


def get_url(fn):
    """
    Use to set the GCP credentials needed
    Parameters
    ----------
    params  (dict) : GCP parameters

    Returns
    -------
    Nothing
    """

    url_info = gcp_config.gcip_rest_urls.get(fn, None)

    if url_info is None:
        return None

    return {
        'url': f"{url_info['url']}?key={gcp_config.api_key}",
        'request_type': url_info.get('request_type', '')
    }

def end_routine(msg):
    """
    """
    
    params = {'error': True,
                'success': False,
                'message': msg,
                'data': None}
    return resp.Response(params)
