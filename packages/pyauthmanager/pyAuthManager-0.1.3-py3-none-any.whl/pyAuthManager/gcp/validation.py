# -*- coding: utf-8 -*-
"""Module description

In this module will be implemented all functions needed to sign up a user with GCP Identity Platform.
The covered functions will be the following :
---- Token Validation
---- Token Refresh
"""
from firebase_admin import auth

import json
import requests

import pyAuthManager.funcs as funcs
import pyAuthManager.gcp as gcp
import pyAuthManager.libs.response as resp


def validate(token, is_access_token=True):
    """
    Sign up a new user to the User Pool set
    Parameters
    ----------
    token (str) : Token to validate

    Returns
    -------
    response (res.Response) : A response object with the status of the request. \
        error is True or False \
        success is True or False
        message is humanely understable message
        data is a possible data to be used
    """

    try:
        claims = auth.verify_id_token(
            token, app=gcp.gcp_config.app, check_revoked=True)

        url_info = gcp.get_url('get_user_data')

        if url_info is None:
            return gcp.end_routine('Action not allowed')

        response = requests.post(url_info['url'], data={
            'idToken': token,
        })

        response.raise_for_status()
        data = response.json()

        claims['email'] = data['users'][0]['email']

        # now we can use the claims
        params = {'error': False,
                  'success': True,
                  'message': "Token was successfully validated",
                  'data': claims}
        return resp.Response(params)

    except auth.InvalidIdTokenError:
        params = {'error': True, 'success': False,
                  'message': "Invalid token"}
        return resp.Response(params)
    except auth.ExpiredIdTokenError:
        params = {'error': True, 'success': False,
                  'message': "Expired token"}
        return resp.Response(params)
    except auth.RevokedIdTokenError:
        params = {'error': True, 'success': False,
                  'message': "Revoked token"}
        return resp.Response(params)
    except auth.CertificateFetchError:
        params = {'error': True, 'success': False,
                  'message': "Certificate fetch error"}
        return resp.Response(params)
    except auth.UserDisabledError:
        params = {'error': True, 'success': False,
                  'message': "User disabled"}
        return resp.Response(params)
    except Exception as e:
        params = {'error': True, 'success': False,
                  'message': f"{e.__str__()}"}
        return resp.Response(params)


def refresh_token(email, refresh_token):
    """
    Sign up a new user to the User Pool set
    Parameters
    ----------
    email        (str) : email of the user
    refresh_token   (str) : refresh token of the existing id_token

    Returns
    -------
    response (res.Response) : A response object with the status of the request. \
        error is True or False \
        success is True or False
        message is humanely understable message
        data is a possible data to be used
    """

    try:
        url_info = gcp.get_url('refresh_token')

        if url_info is None:
            return gcp.end_routine('Action not allowed')

        response = requests.post(url_info['url'], data={
            'grant_type': 'refresh_token',
            'refresh_token': refresh_token,
        })

        response.raise_for_status()
        data = response.json()

    except Exception as e:
        return gcp.end_routine(str(e))

    params = {'error': False,
              'success': True,
              'message': "Successfully signed in the system",
              'data': {
                  "id_token": data["id_token"],
                  'refresh_token': data['refresh_token'],
                  "access_token": data["access_token"],
                  "expires_in": data["expires_in"],
                  "token_type": data["token_type"],
              }}
    return resp.Response(params)
