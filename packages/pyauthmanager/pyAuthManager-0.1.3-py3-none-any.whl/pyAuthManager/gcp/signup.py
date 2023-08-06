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


def sign_up(email, password, name):
    """
    Sign up a new user to the User Pool set
    Parameters
    ----------
    email    (str) : User given email address
    password (str) : User given password
    name     (str) : User given name

    Returns
    -------
    response (res.Response) : A response object with the status of the request. \
        error is True or False \
        success is True or False
        message is humanely understable message
        data is a possible data to be used
    """

    try:
        url_info = gcp.get_url('signup')

        if url_info is None:
            return gcp.end_routine('Action not allowed')

        response = requests.post(url_info['url'], data={
            'email': email,
            'password': password,
            'returnSecureToken': True,
        })

        response.raise_for_status()
        data = response.json()

        url_info = gcp.get_url('update_profile')

        if url_info is None:
            return gcp.end_routine('Action not allowed')

        response = requests.post(url_info['url'], data={
            'idToken': data["idToken"],
            'displayName': name,
            'returnSecureToken': True,
        })

        response.raise_for_status()

        url_info = gcp.get_url('send_verify_mail')
        response = requests.post(url_info['url'], data={
            'requestType': url_info['request_type'],
            'idToken': data["idToken"],
        })

        response.raise_for_status()
        data = response.json()

        if data['email'] != email:
            return gcp.end_routine('Action not allowed')

    except Exception as e:
        return gcp.end_routine(str(e))

    params = {'error': False,
              'success': True,
              'message': "Please confirm your sign-up, check Email for validation code",
              'data': None}
    return resp.Response(params)


def confirm_sign_up(email, code):
    """
    Sign up a new user to the User Pool set
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
        url_info = gcp.get_url('confirm_mail_verification')

        if url_info is None:
            return gcp.end_routine('Action not allowed')

        response = requests.post(url_info['url'], data={
            'oobCode': code,
        })

        response.raise_for_status()
        data = response.json()

        if data['email'] != email or data['emailVerified'] is not True:
            return gcp.end_routine('Access forbidden')

    except Exception as e:
        return gcp.end_routine(str(e))

    params = {'error': False,
              'success': True,
              'message': "Please confirm your sign-up, check Email for validation code",
              'data': None}
    return resp.Response(params)
