from django.db import transaction
from django.utils import timezone

# import models
from accounts.models import CustomUser, StudentProfile, StudentAcademicInfo, StudentParentsInfo, StudentContactInfo, StudentHealthInfo
from accounts.models import TeacherContactInfo, TeacherProfile, TeacherProfessionalInfo
from accounts.models import StaffProfile, AdminProfile, AdminContactInfo, StaffContactInfo

# import exceptions
from rest_framework.exceptions import NotFound

# create helper hare



def verify_user(user:CustomUser):
    user.is_verified = True
    user.save(update_fields=["is_verified"])


from rest_framework_simplejwt.token_blacklist.models import BlacklistedToken, OutstandingToken
def invalidate_user_tokens(user):
    tokens = OutstandingToken.objects.filter(user=user)
    for token in tokens:
        BlacklistedToken.objects.get_or_create(token=token)

    
# update password helper 
def update_password(user:CustomUser, password:str):
    user.set_password(password)
    user.save(update_fields=["password"])
    return user

def update_token_password(user:CustomUser, password:str):
    invalidate_user_tokens(user=user)
    user = update_password(user=user, password=password)
    return user



from rest_framework import serializers
# check previous password helper 
def check_prevues_password(old_password:str, new_password:str) -> bool:
    from django.contrib.auth.hashers import check_password
    if check_password(old_password, new_password):
        raise serializers.ValidationError({"new_password":  "This password has been used previously. Please choose a new one."})


from rest_framework.exceptions import ValidationError
import uuid as uuid_lib

def is_uuid_or_none(value):
    if not value:
        raise ValidationError({"uuid": "UUID is required"})
    try:
        uuid_lib.UUID(str(value))
    except Exception:
        raise ValidationError({"uuid": "Invalid UUID"})


    
    