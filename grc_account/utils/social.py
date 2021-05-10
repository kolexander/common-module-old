from grc_account.models import SocialAccount
from django.contrib.auth import get_user_model
from grc_account.exceptions import UserAlreadyExists
from rest_framework_jwt.settings import api_settings


class SocialService(object):
    @staticmethod
    def create(data, platform):
        """
        Parse data and create account. Raise exception if account with email already exist
        @param data:
        @param platform:
        @return:
        """
        try:
            social_profile = SocialAccount.objects.get(
                social_id=data['social_id'], social_type=data['social_type']
            )
            if social_profile.user is not None:
                return social_profile.user
        except SocialAccount.DoesNotExist:
            social_profile = SocialAccount(social_id=data['social_id'], social_type=data['social_type'])
            social_profile.save()

        try:
            account = get_user_model().objects.get(email=data['email'])
        except get_user_model().DoesNotExist:
            account = get_user_model()(
                first_name=data['first_name'],
                last_name=data['last_name'],
                email=data['email'],
                username=data['social_id'])

        social_profile.user = account
        social_profile.save()

        return account

    @staticmethod
    def obtain_token(user):
        jwt_payload_handler = api_settings.JWT_PAYLOAD_HANDLER
        jwt_encode_handler = api_settings.JWT_ENCODE_HANDLER

        payload = jwt_payload_handler(user)
        token = jwt_encode_handler(payload)

        return token
