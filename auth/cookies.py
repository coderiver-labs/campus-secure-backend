from urllib import request
from django.conf import settings
from django.middleware.csrf import get_token
from django.http import HttpRequest
from django.http import HttpResponse

# import rest_framework
from rest_framework.response import Response
from rest_framework import status
from rest_framework_simplejwt.tokens import RefreshToken


# import models hare
from accounts.models import CustomUser


# import simpleJWT
from rest_framework_simplejwt.tokens import RefreshToken


# import other classes or functions
from typing import Optional


# create your cookie handler hare 




class CookieHandler():
    
    def __init__(self, request:HttpRequest, user:object=None, response:Response=None):
        self.request = request
        self.user = user
        self.response = response or Response(status=status.HTTP_200_OK)
    
    def _common_settings (self) -> dict:
        return {
            "httponly":True,
            "samesite":settings.SIMPLE_JWT.get("AUTH_COOKIE_SAMESITE"),
            "secure":settings.SIMPLE_JWT.get("AUTH_COOKIE_SECURE"),
            "path":settings.SIMPLE_JWT.get("AUTH_COOKIE_PATH")
        }

    def set_cookie(self, key, value, max_age=None) -> None:
        self.response.set_cookie(key=key, value=value, max_age=max_age,**self._common_settings())
        
        
    def set_refresh_token(self, refresh_token) -> None:
        key = settings.SIMPLE_JWT.get("AUTH_COOKIE_REFRESH")
        max_age = settings.COOKIE_MAX_AGE.get("refresh_token")
        self.set_cookie(key=key, value=refresh_token, max_age=max_age)

    def set_access_token(self, access_token) -> None:
        key = settings.SIMPLE_JWT.get("AUTH_COOKIE")
        max_age = settings.COOKIE_MAX_AGE.get("access_token")
        self.set_cookie(key=key, value=access_token, max_age=max_age)
        

    def set_csrf_token(self):
        csrf_token = get_token(request=self.request)
        self.response.set_cookie(
            key=settings.CSRF_COOKIE_NAME,
            value=csrf_token,
            
            httponly=False, # False jate React/JS theke access korte pare :) # akhne aiktu change korte hobe , jodi ami http only ke pop kori tahole r ai line likhte hobena
            samesite=settings.SIMPLE_JWT.get("AUTH_COOKIE_SAMESITE"),
            secure=settings.SIMPLE_JWT.get("AUTH_COOKIE_SECURE"),
            path=settings.SIMPLE_JWT.get("AUTH_COOKIE_PATH"),
        )
    

    def set_last_login(self):
        from django.contrib.auth.models import update_last_login
        update_last_login(sender=None, user=self.user)



    def delete_token(self):
        from .validators import validate_refresh_token
        
        refresh_token = self.request.COOKIES.get("refresh_token")
        refresh_token = validate_refresh_token(request=self.request)
        
        RefreshToken(str(refresh_token)).blacklist()
        response = self.response
        response.delete_cookie("access_token")
        response.delete_cookie("refresh_token")
        response.delete_cookie("csrftoken")


    def get_response(self) -> Response:
        return self.response
    
    

# cookie manager
class AuthCookieService:
    def __init__(self, request:HttpRequest, user:CustomUser):
        self.request = request
        self.user = user

    def issue_tokens(self) -> tuple[str, str]:
        refresh = RefreshToken.for_user(self.user)
        access = refresh.access_token
        return str(access), str(refresh)
    
    def set_login_cookies(self, response:HttpResponse) -> HttpResponse:
        access, refresh = self.issue_tokens()
        cookie = CookieHandler(request=self.request, user=self.user, response=response)
        cookie.set_access_token(access)
        cookie.set_refresh_token(refresh)
        cookie.set_last_login()
        cookie.set_csrf_token()
        return cookie.get_response()

    def set_logout_cookies(self, response:HttpResponse) -> HttpResponse:
        cookie = CookieHandler(request=self.request, user=self.user, response=response)
        cookie.delete_token()
        return cookie.get_response()
    