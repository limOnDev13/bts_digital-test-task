"""The module responsible for sending emails."""

import smtplib
from logging import getLogger

from django.conf import settings

EMAIL_TEXT: str = (
    "Добрый день!\n"
    "Недавно вы интересовались нашим роботом"
    " модели {model}, версии {version}.\n"
    "Этот робот теперь в наличии."
    " Если вам подходит этот вариант - пожалуйста, свяжитесь с нами"
)

logger = getLogger("view.email")


def send_email(email: str, model: str, version: str) -> None:
    """Send an email about this model and version."""
    sender = settings.EMAIL
    sender_password = settings.EMAIL_PASSWORD

    try:
        logger.debug("Connecting...")
        mail_lib = smtplib.SMTP_SSL(settings.SMTP_HOST, settings.SMTP_PORT)
        logger.debug("Login...")
        mail_lib.login(sender, sender_password)

        msg = (
            "From: %s\r\nTo: %s\r\n"
            'Content-Type: text/plain; charset="utf-8"\r\nSubject: %s\r\n\r\n'
            % (sender, email, f"{model}-{version} появился в наличии!")
        )
        msg += EMAIL_TEXT.format(model=model, version=version)

        logger.debug("Sending email...")
        mail_lib.sendmail(sender, email, msg.encode("utf8"))
        mail_lib.quit()
        logger.debug("The email was sent successfully")
    except Exception as exc:
        logger.exception("Error when sending an email. exc=%s", str(exc))
