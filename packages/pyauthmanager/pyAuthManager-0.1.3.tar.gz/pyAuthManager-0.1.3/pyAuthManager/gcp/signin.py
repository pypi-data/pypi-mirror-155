# -*- coding: utf-8 -*-
"""Module description

In this module will be implemented all functions needed to sign up a user with AWS Cognito.
The covered functions will be the following :
---- User sign-up
---- User Sign-up confirmation
"""
import json
import requests

import pyAuthManager.funcs as funcs
import pyAuthManager.gcp as gcp
import pyAuthManager.libs.response as resp


def sign_in(email, password):
    """
    Signs in the user through AWS Cognito
    Parameters
    ----------
    email (str) : User given email
    password (str) : User given password

    Returns
    -------
    response (res.Response) : A response object with the status of the request. \
        error is True or False \
        success is True or False
        message is humanely understable message
        data is a possible data to be used
    """

    try:
        url_info = gcp.get_url('signin_with_pwd')

        if url_info is None:
            return gcp.end_routine('Action not allowed')

        response = requests.post(url_info['url'], data={
            'email': email,
            'password': password,
            'returnSecureToken': True,
        })

        response.raise_for_status()
        data = response.json()

    except Exception as e:
        return gcp.end_routine(str(e))

    params = {'error': False,
              'success': True,
              'message': "Successfully signed in the system",
              'data': {
                  'id_token': data['idToken'],
                  'refresh_token': data['refreshToken'],
                  'access_token': data['idToken'],
                  'expires_in': data['expiresIn'],
                  'token_type': None,
              }}
    return resp.Response(params)
