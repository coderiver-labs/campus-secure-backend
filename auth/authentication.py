from rest_framework_simplejwt.authentication import JWTAuthentication
from rest_framework.exceptions import AuthenticationFailed
from rest_framework_simplejwt.exceptions import ExpiredTokenError, TokenError, InvalidToken 
from rest_framework_simplejwt.tokens import AccessToken, RefreshToken

# import others 
from django.http import HttpRequest

# import logger 
from utils.constants import JWT_ERROR_MESSAGES


# create your cookie base auth hare


# check refresh token
def check_validate_refresh_token(refresh_token: str, request=None, user=None) -> RefreshToken:
    """
    Validate the given refresh token string.
    Raise AuthenticationFailed with proper messages if invalid.
    """
    try:
        token = RefreshToken(refresh_token)
        return token
    except ExpiredTokenError:
        raise AuthenticationFailed("Expired Refresh token, Please Log in again")

    except InvalidToken:
        raise AuthenticationFailed("Invalid refresh token. Please log in again.")
    except TokenError:
        raise AuthenticationFailed("Invalid refresh token. Please log in again.")



# csrf authentications 
from rest_framework.authentication import BasicAuthentication
from django.middleware.csrf import CsrfViewMiddleware
from django.conf import settings
class CSRFAuthentication(BasicAuthentication):
    """
    Runs Django's CSRF validation for incoming request.
    Returns None since this class doesn't authenticate users — only validates CSRF.
    """
    def authenticate(self, request):
        csrf_middleware = CsrfViewMiddleware(lambda req:None)
        reason = csrf_middleware.process_view(request=request, callback=None, callback_args=(), callback_kwargs={})
        if reason:
            raise AuthenticationFailed("CSRF validation failed")
        return None


# JWT Authentication for user 
class UserAuthentication(JWTAuthentication):
    """
    Cookie-based JWT authentication with strict validation.
    """
    
    def authenticate(self, request: HttpRequest):
        from auth.validators import validate_access_token, get_valid_user
        validated_token = validate_access_token(request)
        user = self.get_user(validated_token)
        user = get_valid_user(user)
        return (user, validated_token)
    