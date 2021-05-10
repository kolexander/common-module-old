from django.core.mail import send_mail


class Mail(object):
    @staticmethod
    def send(subject: str, message: str, from_email: str, to_email: str, html_message=None) -> bool:
        """
        Send email
        :param subject:
        :param message:
        :param from_email:
        :param to_email:
        :param html_message:
        :return:
        """
        return send_mail(
            subject,
            message,
            from_email,
            [to_email],
            html_message=html_message,
            fail_silently=False,
        )