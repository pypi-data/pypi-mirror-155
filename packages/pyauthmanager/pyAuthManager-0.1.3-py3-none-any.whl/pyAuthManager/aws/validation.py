import boto3
import botocore.exceptions
import json
import time
import urllib.request
from jose import jwk, jwt
from jose.utils import base64url_decode

import pyAuthManager.funcs as funcs
import pyAuthManager.aws as aws
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

    # get the kid from the headers prior to verification
    headers = jwt.get_unverified_headers(token)
    kid = headers['kid']
    # search for the kid in the downloaded public keys
    key_index = -1
    for i in range(len(aws.aws_config.keys)):
        if kid == aws.aws_config.keys[i]['kid']:
            key_index = i
            break

    if key_index == -1:
        params = {'error': True,
                  'success': False,
                  'message': "Public key not found in jwks.json",
                  'data': None}
        return resp.Response(params)

    # construct the public key
    public_key = jwk.construct(aws.aws_config.keys[key_index])

    # get the last two sections of the token,
    # message and signature (encoded in base64)
    message, encoded_signature = str(token).rsplit('.', 1)

    # decode the signature
    decoded_signature = base64url_decode(encoded_signature.encode('utf-8'))

    # verify the signature
    if not public_key.verify(message.encode("utf8"), decoded_signature):
        params = {'error': True,
                  'success': False,
                  'message': "Signature verification failed",
                  'data': None}
        return resp.Response(params)

    # since we passed the verification, we can now safely
    # use the unverified claims
    claims = jwt.get_unverified_claims(token)

    # additionally we can verify the token expiration
    if time.time() > claims['exp']:
        params = {'error': True,
                  'success': False,
                  'message': "Token is expired",
                  'data': None}
        return resp.Response(params)

    audience = 'client_id'
    if is_access_token is False:
        audience = 'aud'

    if claims[audience] != aws.aws_config.client_id:
        params = {'error': True,
                  'success': False,
                  'message': "Token was not issued for this audience",
                  'data': None}
        return resp.Response(params)

    # now we can use the claims
    params = {'error': False,
              'success': True,
              'message': "Token was successfully validated",
              'data': claims}
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

    params = {}
    client = aws.aws_config.client
    try:
        secret_hash = funcs.get_secret_hash(email)
        result = client.initiate_auth(
            AuthParameters={
                'USERNAME': email,
                'SECRET_HASH': secret_hash,
                'REFRESH_TOKEN': refresh_token,

            },
            ClientId=aws.aws_config.client_id,
            AuthFlow='REFRESH_TOKEN_AUTH',
        )
        res = result.get("AuthenticationResult")

    except client.exceptions.NotAuthorizedException as e:
        params = {
            'message': "Invalid refresh token or email is incorrect or Refresh Token has been revoked"}
        return resp.Response(params)
    except client.exceptions.UserNotConfirmedException as e:
        params = {'message': "User is not confirmed"}
        return resp.Response(params)
    except Exception as e:
        params = {'message': e.__str__()}
        return resp.Response(params)

    if res:
        params = {'message': 'success',
                  'error': False,
                  'success': True,
                  'data': {
                      "id_token": res["IdToken"],
                      "access_token": res["AccessToken"],
                      "refresh_token": res["RefreshToken"],
                      "expires_in": res["ExpiresIn"],
                      "token_type": res["TokenType"],
                  }}
        return resp.Response(params)

    params = {'message': None}
    return resp.Response(params)
