from datetime import timedelta
from urllib.parse import quote

from django.conf import settings
from django.utils import timezone

from grc_account.models import get_password_reset_token_expiry_time
from grc_account.utils.hash_generator import generate
from django.contrib.auth import get_user_model


class Confirmations(object):
    @staticmethod
    def generate_code() -> str:
        """
        Generate code
        @return:
        """
        return generate(amount=27)

    @staticmethod
    def generate_url_with_email(endpoint: str, email: str, code: str) -> str:
        """
        Generate url for email
        @param endpoint:
        @param email:
        @param code:
        @return:
        """
        url = endpoint + '?email=' + quote(email) + '&code=' + code

        return url

    @staticmethod
    def generate_url_without_email(endpoint: str, code: str) -> str:
        """
        Generate url for email
        @param endpoint:
        @param code:
        @return:
        """
        url = endpoint + '?code=' + code

        return url

    @staticmethod
    def validate(username: str, code: str) -> bool:
        return get_user_model().objects.filter(username=username, confirmation_code=code).exists()


class PasswordResetConfirmation(Confirmations):
    @staticmethod
    def get_url(username: str, code: str) -> str:
        if '@' in username:
            url = super(EmailConfirmation, EmailConfirmation).generate_url_without_email(
                settings.PASSWORD_RESET_CONFIRMATION_ENDPOINT,
                code)
        else:
            url = None
        return url

    @staticmethod
    def validate(account, code):
        password_reset_token_validation_time = int(get_password_reset_token_expiry_time())

        expiry_date = account.reset_password_token_created_at + timedelta(
            hours=password_reset_token_validation_time)

        if timezone.now() > expiry_date:
            return False

        return account.reset_password_token == code

    @staticmethod
    def generate_code(username: str) -> str:
        """
        Generate code
        @return:
        """

        if '@' in username:
            return Confirmations.generate_code()
        return '1111'

