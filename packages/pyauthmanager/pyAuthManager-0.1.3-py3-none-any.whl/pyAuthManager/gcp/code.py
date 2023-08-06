"""Module description

In this module will be implemented all functions needed to manage user pool passwords with AWS Cognito.
The covered functions will be the following :
---- forgot password
---- Confirm forgot password
"""
import json
import requests

import pyAuthManager.funcs as funcs
import pyAuthManager.gcp as gcp
import pyAuthManager.libs.response as resp


def forgot_password(email):
    """
    Forgot password for an user to the User Pool set
    Parameters
    ----------
    email (str) : User given email

    Returns
    -------
    response (res.Response) : A response object with the status of the request. \
        error is True or False \
        success is True or False
        message is humanely understable message
        data is a possible data to be used
    """

    try:
        url_info = gcp.get_url('send_pwd_reset_mail')

        if url_info is None:
            return gcp.end_routine('Action not allowed')

        response = requests.post(url_info['url'], data={
            'email': email,
            'requestType': url_info['request_type'],
        })

        response.raise_for_status()
        data = response.json()

    except Exception as e:
        return gcp.end_routine(str(e))

    params = {'error': False,
              'success': True,
              'message': "Successfully signed in the system",
              'data': data}
    return resp.Response(params)


def confirm_forgot_password(email, password, code):
    """
    Confirm forgot password for an user of the User Pool set
    Parameters
    ----------
    email (str) : User given email
    password (str) : User given password
    code     (str) : User given name

    Returns
    -------
    response (res.Response) : A response object with the status of the request. \
        error is True or False \
        success is True or False
        message is humanely understable message
        data is a possible data to be used
    """

    try:
        url_info = gcp.get_url('confirm_pwd_reset')

        if url_info is None:
            return gcp.end_routine('Action not allowed')

        response = requests.post(url_info['url'], data={
            'oobCode': password,
            'newPassword': code,
        })

        response.raise_for_status()
        data = response.json()

    except Exception as e:
        return gcp.end_routine(str(e))

    params = {'error': False,
              'success': True,
              'message': "Successfully signed in the system",
              'data': data}
    return resp.Response(params)
