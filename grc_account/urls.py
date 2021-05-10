from django.conf.urls import url, include
from rest_framework.routers import DefaultRouter
from rest_framework_jwt.views import refresh_jwt_token, verify_jwt_token

from grc_account.views import AuthView, RequestResetPasswordView, ConfirmResetPasswordView, \
    AccountView, ChangePasswordView, SocialAuthView

app_name = 'account'

router = DefaultRouter()
# introduction
router.register(r'me', AccountView, basename='me')
router.register('social_auth/', SocialAuthView, basename='social_auth'),

urlpatterns = [
    # auth + jwt
    url('auth/', AuthView.as_view(), name='auth'),
    url(r'^token-refresh/', refresh_jwt_token),
    url(r'^token-verify/', verify_jwt_token),

    # Reset password
    url('reset-password/confirm/', ConfirmResetPasswordView.as_view(), name='confirm-reset-password'),
    url('reset-password/', RequestResetPasswordView.as_view(), name='request-reset-password'),

    # Change password
    url('change-password/', ChangePasswordView.as_view(), name='change-password'),
]

urlpatterns += router.urls


