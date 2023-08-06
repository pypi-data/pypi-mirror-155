import pyAuthManager.init as init
import pyAuthManager.aws.signup as aws_signup
import pyAuthManager.aws.code as aws_code
import pyAuthManager.aws.signin as aws_signin
import pyAuthManager.aws.validation as aws_validation
import pyAuthManager.gcp.signup as gcp_signup
import pyAuthManager.gcp.code as gcp_code
import pyAuthManager.gcp.signin as gcp_signin
import pyAuthManager.gcp.validation as gcp_validation


def __raise_invalid_provider():
    """
    Raise an invalid provider exception
    Parameters
    ----------
    None

    Returns
    -------
    Nothing
    """

    raise Exception("Invalid provider given !!!")


class Constant:
    pass


constant = Constant()
constant.aws = 'aws'
constant.gcp = 'gcp'
constant.azure = 'azure'


class Config:
    pass


provider_config = Config()
provider_config.provider = constant.aws

set_provider_switcher = {
    constant.aws: init.__init_aws,
    constant.gcp: init.__init_gcp,
    constant.azure: init.__init_azure,
}

sign_up_switcher = {
    constant.aws: aws_signup.sign_up,
    constant.gcp: gcp_signup.sign_up,
}

confirm_sign_up_switcher = {
    constant.aws: aws_signup.confirm_sign_up,
    constant.gcp: gcp_signup.confirm_sign_up,
}

forgot_password_switcher = {
    constant.aws: aws_code.forgot_password,
    constant.gcp: gcp_code.forgot_password,
}

confirm_forgot_password_switcher = {
    constant.aws: aws_code.confirm_forgot_password,
    constant.gcp: gcp_code.confirm_forgot_password,
}

validate_switcher = {
    constant.aws: aws_validation.validate,
    constant.gcp: gcp_validation.validate,
}

refresh_token_switcher = {
    constant.aws: aws_validation.refresh_token,
    constant.gcp: gcp_validation.refresh_token,
}


def set_provider(provider):
    """
    Sign in a not real user to the User Pool set
    Parameters
    ----------
    provider    (str) : cloud provider

    Returns
    -------
    Nothing
    """

    provider_config.provider = provider
    fn = set_provider_switcher.get(provider, __raise_invalid_provider)
    fn()


def sign_up(email, password, name):
    """
    Sign up a new user
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

    fn = sign_up_switcher.get(provider_config.provider,
                              __raise_invalid_provider)
    return fn(email, password, name)


def confirm_sign_up(email, code):
    """
    Sign up a new user
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

    fn = confirm_sign_up_switcher.get(
        provider_config.provider, __raise_invalid_provider)
    return fn(email, code)


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

    fn = forgot_password_switcher.get(
        provider_config.provider, __raise_invalid_provider)
    return fn(email)


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

    fn = confirm_forgot_password_switcher.get(
        provider_config.provider, __raise_invalid_provider)
    return fn(email, password, code)


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

    switcher = {
        constant.aws: aws_signin.sign_in,
        constant.gcp: gcp_signin.sign_in,
    }

    fn = switcher.get(provider_config.provider, __raise_invalid_provider)
    return fn(email, password)


def validate(token):
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

    fn = validate_switcher.get(
        provider_config.provider, __raise_invalid_provider)
    return fn(token)


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

    fn = refresh_token_switcher.get(
        provider_config.provider, __raise_invalid_provider)
    return fn(email, refresh_token)
