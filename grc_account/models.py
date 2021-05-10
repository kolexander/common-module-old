from django.contrib.auth.models import AbstractUser, BaseUserManager
from django.db import models
from django.conf import settings
from phonenumber_field.modelfields import PhoneNumberField
from django.utils.translation import gettext_lazy as _
from django.contrib.auth import get_user_model


class AbstractAccount(AbstractUser):
    """
    Account model
    """

    email = models.EmailField(null=True, blank=True)
    phone = PhoneNumberField(null=True, blank=True)
    username = models.CharField(max_length=50, unique=True)
    confirmation_code = models.CharField(max_length=255, null=True, blank=True)
    is_done = models.BooleanField(default=False)  # is registration done
    reset_password_token = models.CharField(null=True, unique=True, max_length=30, blank=True)
    reset_password_token_created_at = models.DateTimeField(null=True)
    is_active = models.BooleanField(
        _('active'),
        default=False,
        help_text=_(
            'Designates whether this user should be treated as active. '
            'Unselect this instead of deleting accounts.'
        ),
    )

    USERNAME_FIELD = 'username'
    REQUIRED_FIELDS = []

    class Meta:
        db_table = 'users'
        verbose_name = 'Account'
        verbose_name_plural = 'Accounts'
        unique_together = ('email', 'phone')
        abstract = True


class SocialAccount(models.Model):
    """
        Social account model
    """

    class SocialType(models.IntegerChoices):
        LINKEDIN = 1
        FACEBOOK = 2
        GOOGLE = 3

    social_id = models.CharField(max_length=150)
    account = models.ForeignKey(
        get_user_model(), verbose_name='social_account',
        null=False, on_delete=models.CASCADE
    )
    social_type = models.IntegerField(choices=SocialType.choices)

    class Meta:
        db_table = 'social_account'
        verbose_name = 'Social account'
        verbose_name_plural = 'Social accounts'


def get_password_reset_token_expiry_time():
    """
    Returns the password reset token expiry time in hours (default: 24)
    """
    # get token validation time
    return getattr(settings, 'RESET_PASSWORD_EXPIRY', 24)
