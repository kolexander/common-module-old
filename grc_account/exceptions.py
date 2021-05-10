from rest_framework import status
from rest_framework.exceptions import APIException


class UserNotFoundLogin(APIException):
    status_code = status.HTTP_404_NOT_FOUND
    default_detail = 'We don’t see an account linked to this email.'
    default_code = 'user_not_found'


class UserNotFoundLostPassword(APIException):
    status_code = status.HTTP_404_NOT_FOUND
    default_detail = 'There is no such account'
    default_code = 'user_not_found'


class UserAlreadyExists(APIException):
    status_code = status.HTTP_400_BAD_REQUEST
    default_detail = 'User already exists'
    default_code = 'user_already_exists'


class IncorrectInputPassword(APIException):
    status_code = status.HTTP_400_BAD_REQUEST
    default_detail = 'Your password must be 8 or more characters, contain at least one uppercase, one lowercase, ' \
                     'one symbol and one number. Example: P@$$W0rD1 '
    default_code = 'incorrect_input_password'


class UserNotConfirmEmail(APIException):
    status_code = status.HTTP_403_FORBIDDEN
    default_detail = 'Confirm email'
    default_code = 'confirm_email'


class TokenExpired(APIException):
    status_code = status.HTTP_400_BAD_REQUEST
    default_detail = 'Token Expired'
    default_code = 'token_expired'


class IncorrectPassword(APIException):
    status_code = status.HTTP_400_BAD_REQUEST
    default_detail = 'The password is not correct.'
    default_code = 'incorrect_password'
