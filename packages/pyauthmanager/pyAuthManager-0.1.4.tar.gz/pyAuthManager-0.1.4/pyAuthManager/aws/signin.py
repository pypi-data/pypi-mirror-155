"""Module description

In this module will be implemented all functions needed to authenticate an user  with AWS Cognito.
The covered functions will be the following :
---- initiate user authorization
---- **lambda function**
"""
import boto3
import botocore.exceptions
import json

import pyAuthManager.funcs as funcs
import pyAuthManager.aws as aws
import pyAuthManager.libs.response as resp


def __initiate_auth(client, email, password):
    """
    Initiate authorization of user of the User Pool set
    Parameters
    ----------
    client   (boto3.client) : aws boto3 client to connect to aws service
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
        secret_hash = funcs.get_secret_hash(
            aws.aws_config.client_id, aws.aws_config.client_secret, email)
        data = client.admin_initiate_auth(
            UserPoolId=aws.aws_config.user_pool_id,
            ClientId=aws.aws_config.client_id,
            AuthFlow='ADMIN_USER_PASSWORD_AUTH',
            AuthParameters={
                'USERNAME': email,
                'SECRET_HASH': secret_hash,
                'PASSWORD': password,
            },
            ClientMetadata={
                'email': email,
                'password': password,
            })
    except client.exceptions.NotAuthorizedException:
        params = {'error': True, 'success': False,
                  'message': "The email or password is incorrect"}
        return resp.Response(params)
    except client.exceptions.UserNotConfirmedException:
        params = {'error': True, 'success': False,
                  'message': "User is not confirmed"}
        return resp.Response(params)
    except Exception as e:
        params = {'error': True, 'success': False,
                  'message': f"{e.__str__()}"}
        return resp.Response(params)

    params = {'error': False, 'success': True,
              'message': "Authorization successfully completed", 'data': data}
    return resp.Response(params)


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

    params = {}
    client = aws.aws_config.client

    res = __initiate_auth(client, email, password)
    if res.error is True:
        return res

    data = res.data
    if data.get("AuthenticationResult"):
        params = {'message': 'success',
                  'error': False,
                  'success': True,
                  'data': {
                      "id_token": data["AuthenticationResult"]["IdToken"],
                      "refresh_token": data["AuthenticationResult"]["RefreshToken"],
                      "access_token": data["AuthenticationResult"]["AccessToken"],
                      "expires_in": data["AuthenticationResult"]["ExpiresIn"],
                      "token_type": data["AuthenticationResult"]["TokenType"]
                  }}
    else:  # this code block is relevant only when MFA is enabled
        params = {'error': True, 'success': False,
                  'data': None, 'message': None}

    return resp.Response(params)
