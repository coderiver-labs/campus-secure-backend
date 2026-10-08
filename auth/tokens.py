# django imports
from django.utils import timezone
from datetime import timedelta

# import models hare
from accounts.models import CustomUser, OneTimeToken

# import settings
from django.conf import settings

# import config
from decouple import config

# import python built-in
import secrets
import hmac
import hashlib


# create one time token
def create_token(user:CustomUser, purpose:str, expiry_minutes:timedelta=int(30)):
    row = secrets.token_urlsafe(32)
    payload = f"{row}|{user.uuid}|{purpose}|{user.password}"
    signature = hmac.new(settings.TOKEN_SIGNING_KEY.encode(), payload.encode(), hashlib.sha256).hexdigest()
    signed = f"{row}.{signature}"
    token_hash = hashlib.sha256(signed.encode()).hexdigest()
    OneTimeToken.objects.update_or_create(user=user, defaults={"purpose": purpose, "token":token_hash, "expired_at": timezone.now()+timedelta(minutes=expiry_minutes), "is_used": False})
    return signed



from django import urls
# generate one time url for any work, like email verify or password reset any 
def generate_one_time_url(token:secrets, base_url:urls.path) -> urls:
    domain = settings.FRONTEND_URL
    url = f"{domain}/{base_url}{token}/"
    return url



