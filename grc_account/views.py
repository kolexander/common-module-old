from datetime import datetime

from rest_framework import viewsets, status
from rest_framework.generics import GenericAPIView
from rest_framework.permissions import AllowAny
from rest_framework.response import Response
from rest_framework_jwt.views import JSONWebTokenAPIView

from grc_account.exceptions import TokenExpired, UserNotFoundLostPassword, UserNotFoundLogin
from django.contrib.auth import get_user_model
from grc_account.security.confirmations import Confirmations, PasswordResetConfirmation
from grc_account.serializers import (
    RegisterSerializer, AuthSerializer, UsernameSerializer, ConfirmResetPasswordSerializer,
    RegisterConfirmSerializer, AccountSerializer, ChangePasswordSerializer, SocialAccountSerializer
)
from grc_account.tasks import reset_password_email, reset_password_phone
from grc_account.models import SocialAccount


class AuthView(JSONWebTokenAPIView):
    """
    API View that receives a POST with a user's username and password.

    Returns a JSON Web Token that can be used for authenticated requests.
    """
    serializer_class = AuthSerializer


class RequestResetPasswordView(GenericAPIView):
    serializer_class = UsernameSerializer
    permission_classes = [AllowAny, ]

    def post(self, request):
        """
        Request reset password
        :param request:
        :return: Response()
        """
        serializer = self.serializer_class(data=request.data)
        serializer.is_valid(raise_exception=True)
        username = serializer.validated_data['username']

        try:
            account = get_user_model().objects.get(username=username)
        except get_user_model().DoesNotExist:
            raise UserNotFoundLostPassword()

        if account.is_active:
            code = PasswordResetConfirmation.generate_code(username)
            url = PasswordResetConfirmation.get_url(username, code)
            account.reset_password_token = code
            account.reset_password_token_created_at = datetime.now()
            account.save()

            if '@' in username:
                reset_password_email.delay(username, url)
            else:
                reset_password_phone.delay(username, code)

        return Response(status=status.HTTP_200_OK)


class ConfirmResetPasswordView(GenericAPIView):
    serializer_class = ConfirmResetPasswordSerializer
    permission_classes = [AllowAny, ]

    def post(self, request):
        """
        Reset password
        :param request:
        :return: Response()
        """
        serializer = self.serializer_class(data=request.data)
        serializer.is_valid(raise_exception=True)
        password = serializer.validated_data['password']
        code = serializer.validated_data['code']

        try:
            account = get_user_model().objects.get(reset_password_token=code)
        except get_user_model().DoesNotExist:
            raise UserNotFoundLostPassword()

        is_valid = PasswordResetConfirmation.validate(account=account, code=code)

        if is_valid:
            account.password = password
            account.reset_password_token = None
            account.reset_password_token_created_at = None
            account.save()
        else:
            raise TokenExpired()

        return Response(status=status.HTTP_200_OK)


class AccountView(viewsets.ModelViewSet):
    model_class = get_user_model()
    serializer_class = AccountSerializer
    queryset = get_user_model().objects.all()

    def get_queryset(self):
        """
        Filter account by user pk
        :return: queryset
        """
        user = self.request.user
        queryset = self.queryset.filter(pk=user.pk)

        return queryset

    def list(self, request, *args, **kwargs):
        """
        Redeclared list method to return one instance
        :param request:
        :param args:
        :param kwargs:
        :return: Response()
        """
        try:
            account = self.get_queryset().get()
        except Exception:
            return Response(status=status.HTTP_404_NOT_FOUND)
        serializer = self.get_serializer(account)
        return Response(serializer.data)


class ChangePasswordView(viewsets.ModelViewSet):
    serializer_class = ChangePasswordSerializer

    def put(self, request):
        serializer = self.serializer_class(data=request.data, context={'request': request})
        serializer.is_valid(raise_exception=True)
        password = serializer.validated_data['new_password']

        user = request.user
        user.password = password
        user.save()

        return Response(status=status.HTTP_200_OK)


class SocialAuthView(viewsets.ModelViewSet):
    model_class = SocialAccount
    serializer_class = SocialAccountSerializer
    queryset = SocialAccount.objects.all()
