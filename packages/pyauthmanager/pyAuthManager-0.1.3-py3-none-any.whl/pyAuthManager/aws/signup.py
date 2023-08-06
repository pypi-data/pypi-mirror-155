# -*- coding: utf-8 -*-
"""Module description

In this module will be implemented all functions needed to sign up a user with AWS Cognito.
The covered functions will be the following :
---- User sign-up
---- User Sign-up confirmation
"""

import pyAuthManager.funcs as funcs
import pyAuthManager.aws as aws
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

    client = aws.aws_config.client

    try:
        data = client.sign_up(
            ClientId=aws.aws_config.client_id,
            SecretHash=funcs.get_secret_hash(
                aws.aws_config.client_id, aws.aws_config.client_secret, email),
            Username=email,
            Password=password,
            UserAttributes=[
                {
                    'Name': "name",
                    'Value': name
                },
                {
                    'Name': "email",
                    'Value': email
                }
            ],
            ValidationData=[
                {
                    'Name': "email",
                    'Value': email
                },
            ])
    except client.exceptions.UsernameExistsException as e:
        params = {'error': True,
                  'success': False,
                  'message': "This username already exists",
                  'data': None}
        return resp.Response(params)
    except client.exceptions.InvalidPasswordException as e:
        params = {'error': True,
                  'success': False,
                  'message': "Password should have Caps, Special chars, Numbers",
                  'data': None}
        return resp.Response(params)
    except client.exceptions.UserLambdaValidationException as e:
        params = {'error': True,
                  'success': False,
                  'message': "Email already exists",
                  'data': None}
        return resp.Response(params)
    except Exception as e:
        params = {'error': True,
                  'success': False,
                  'message': str(e),
                  'data': None}
        return resp.Response(params)

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

    client = aws.aws_config.client

    try:
        data = client.confirm_sign_up(
            ClientId=aws.aws_config.client_id,
            SecretHash=funcs.get_secret_hash(
                aws.aws_config.client_id, aws.aws_config.client_secret, email),
            Username=email,
            ConfirmationCode=code,
            ForceAliasCreation=False,
        )
    except client.exceptions.UserNotFoundException:
        params = {'error': True, 'success': False,
                  'message': "Username doesn't exists"}
        return resp.Response(params)
    except client.exceptions.CodeMismatchException:
        params = {'error': True, 'success': False,
                  'message': "Invalid Verification code", 'data': None}
        return resp.Response(params)
    except client.exceptions.NotAuthorizedException:
        params = {'error': True, 'success': False,
                  'message': "User is already confirmed", 'data': None}
        return resp.Response(params)
    except Exception as e:
        params = {'error': True, 'success': False,
                  'message': f"Unknown error {e.__str__()}", 'data': None}
        return resp.Response(params)

    params = {'error': False, 'success': True,
              'message': "Signing up successfully confirmed", 'data': None}
    return resp.Response(params)
