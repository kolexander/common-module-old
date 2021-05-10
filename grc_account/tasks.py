from __future__ import absolute_import, unicode_literals
from celery import shared_task
from django.conf import settings
from django.template.loader import render_to_string

from grc_account.utils.mail import Mail


@shared_task
def reset_password_email(to_email: str, url: str):
    """
    Send reset password email
    :param to_email:
    :param url:
    :return:
    """
    subject = 'Reset Password'
    message = 'Click here ' + url
    context = {
        'url': url
    }
    html_message = render_to_string('reset_password.html', context)

    Mail.send(subject=subject, message=message, from_email=settings.EMAIL_SENDER, to_email=to_email,
              html_message=html_message)

    return None


@shared_task
def reset_password_phone(phone: str, code: str):
    """
    Send reset password email
    :param to_email:
    :param url:
    :return:
    """

    return None
