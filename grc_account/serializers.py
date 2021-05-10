import re

from django.contrib.auth.hashers import make_password
from django.contrib.postgres.fields import ArrayField
from rest_framework import serializers
from rest_framework_jwt.serializers import JSONWebTokenSerializer
from django.contrib.auth import get_user_model
from grc_account.models import SocialAccount
from grc_account.exceptions import IncorrectInputPassword, UserAlreadyExists, UserNotConfirmEmail, \
    IncorrectPassword, UserNotFoundLogin

from grc_account.utils.hash_generator import generate
from grc_account.utils.social import SocialService


class RegisterSerializer(serializers.ModelSerializer):
    username = serializers.CharField(required=True)
    password = serializers.CharField(required=True)
    type = serializers.IntegerField(required=True)

    class Meta:
        model = get_user_model()
        fields = ('username', "password", "type")

    def validate(self, data):
        """
        Validates password, generate username
        @param data:
        @return:
        """
        if 'username' not in data:
            return
        try:
            account = get_user_model().objects.get(username=data['username'])
        except get_user_model().DoesNotExist:
            account = None

        if account is not None:
            raise UserAlreadyExists()

        if data['password']:
            if validate_password(data['password']):
                data['password'] = make_password(data['password'])

        return data


class AuthSerializer(JSONWebTokenSerializer):
    def validate(self, attrs):
        """
        Checks if user already confirm email
        :param attrs:
        :return:
        """
        username = attrs.get(self.username_field)
        try:
            account = get_user_model().objects.get(username=username)
        except get_user_model().DoesNotExist:
            raise UserNotFoundLogin()

        if not account.is_active:
            raise UserNotConfirmEmail()

        try:
            return super().validate(attrs)
        except serializers.ValidationError:
            raise IncorrectPassword()


class UsernameSerializer(serializers.Serializer):
    username = serializers.CharField(required=True)


class ConfirmResetPasswordSerializer(serializers.Serializer):
    password = serializers.CharField(required=True)
    code = serializers.CharField(required=True)

    def validate(self, data):
        if validate_password(data['password']):
            data['password'] = make_password(data['password'])

        return data


class RegisterConfirmSerializer(serializers.Serializer):
    username = serializers.CharField(required=True)
    code = serializers.CharField(required=True)


def validate_password(password: str) -> bool:
    """
    Validate password
    :param password:
    :return:
    """
    regex = re.compile(
        r"^(?=.*[a-z])(?=.*[A-Z])(?=.*\d)(?=.*[-@$!%*?&#^()_=+\\\/.,|{}\[\]»№;:<>~\'\"])[A-Za-z\d\-@$!%*?&#^()_=+\\\/.,|{}\[\]»№;:<>~\'\"]{8,}$")
    if regex.match(password) is None:
        raise IncorrectInputPassword()

    return True


class AccountSerializer(serializers.ModelSerializer):
    first_name = serializers.CharField(required=False)
    last_name = serializers.CharField(required=False, max_length=88)
    username = serializers.CharField(required=False)
    email = serializers.EmailField(read_only=True)
    phone = serializers.CharField(read_only=True)

    class Meta:
        model = get_user_model()
        fields = ('id',
                  'first_name',
                  'last_name',
                  'username',
                  'email',
                  'phone',)


class SocialAccountSerializer(serializers.ModelSerializer):

    class Meta:
        model = SocialAccount
        fields = ('social_id', 'account', 'social_type')

    def create(self, validated_data):
        account = SocialService.create(validated_data)
        data = AccountSerializer(account).data
        data['token'] = SocialService.obtain_token(account)


class ChangePasswordSerializer(serializers.Serializer):
    old_password = serializers.CharField(required=True)
    new_password = serializers.CharField(required=True)

    def validate(self, data):
        """
        Validate old password
        :param data:
        :return:
        """

        user = self.context['request'].user

        if not user.check_password(data['old_password']):
            raise IncorrectPassword()

        if validate_password(data['new_password']):
            data['new_password'] = make_password(data['new_password'])

        return data
