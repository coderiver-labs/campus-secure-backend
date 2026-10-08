from django.core.mail import EmailMultiAlternatives
from django.template.loader import render_to_string
from django.conf import settings

# import typing
from typing import Optional, Dict, List

# errors classes
from django.core.mail import BadHeaderError
from rest_framework.exceptions import ValidationError as DRFValidationError





def send_email(*, to: List[str], subject: str, template: str, context: Dict, request: Optional[object] = None) -> None:
    """
    Universal HTML email sender.
    - to: list of recipient emails
    - subject: email subject
    - template: HTML template path
    - context: context dict for template
    """

    try:
        from_email = settings.EMAIL_HOST_USER
        html_content = render_to_string(template, context)
        email = EmailMultiAlternatives(subject=subject, body="", from_email=from_email, to=to)
        email.attach_alternative(html_content, "text/html")
        email.send()

    except BadHeaderError:
        raise BadHeaderError("Invalid email header")

    except Exception as e:
        raise Exception(f"Email sending failed | {str(e)}")


