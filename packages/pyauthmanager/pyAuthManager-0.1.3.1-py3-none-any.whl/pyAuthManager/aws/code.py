"""Module description

In this module will be implemented all functions needed to manage user pool passwords with AWS Cognito.
The covered functions will be the following :
---- forgot password
---- Confirm forgot password
"""
import boto3
import botocore.exceptions
import json

import pyAuthManager.funcs as funcs
import pyAuthManager.aws as aws
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

    client = aws.aws_config.client

    try:
        data = client.forgot_password(
            ClientId=aws.aws_config.client_id,
            SecretHash=funcs.get_secret_hash(
                aws.aws_config.client_id, aws.aws_config.client_secret, email),
            Username=email
        )
    except client.exceptions.UserNotFoundException:
        params = {'error': True,  'success': False,
                  'message': "Username doesn't exists"}
        return resp.Response(params)
    except client.exceptions.InvalidParameterException:
        params = {'error': True, 'success': False,
                  'message': f"User <{email}> is not confirmed yet"}
        return resp.Response(params)
    except client.exceptions.CodeMismatchException:
        params = {'error': True, 'success': False,
                  'message': "Invalid Verification code"}
        return resp.Response(params)
    except client.exceptions.NotAuthorizedException:
        params = {'error': True, 'success': False,
                  'message': "User is already confirmed"}
        return resp.Response(params)
    except Exception as e:
        params = {'error': True, 'success': False,
                  'message': "Unknown    error {e.__str__()} "}

    params = {'error': False, 'success': True,
              'message': "Please check your Registered email id for validation code", 'data': data}
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
    client = aws.aws_config.client
    try:
        data = client.confirm_forgot_password(
            ClientId=aws.aws_config.client_id,
            SecretHash=funcs.get_secret_hash(
                aws.aws_config.client_id, aws.aws_config.client_secret, email),
            Username=email,
            ConfirmationCode=code,
            Password=password,
        )
    except client.exceptions.UserNotFoundException:
        params = {'error': True, 'success': False,
                  'message': "Username doesn't exists"}
        return resp.Response(params)
    except client.exceptions.CodeMismatchException:
        params = {'error': True, 'success': False,
                  'message': "Invalid Verification code"}
        return resp.Response(params)
    except client.exceptions.NotAuthorizedException:
        params = {'error': True, 'success': False,
                  'message': "User is already confirmed"}
        return resp.Response(params)
    except Exception as e:
        params = {'error': True, 'success': False,
                  'message': f"error {e.__str__()} "}
        return resp.Response(params)

    params = {'error': False, 'success': True,
              'message': "Password has been changed successfully"}
    return resp.Response(params)
