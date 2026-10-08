from drf_spectacular.utils import inline_serializer
from rest_framework import serializers

# create schema

UserBasicInfoSchema = inline_serializer(
    name="UserBasicInfo",
    fields={
        "uuid": serializers.UUIDField(),
        "first_name": serializers.CharField(),
        "last_name": serializers.CharField(),
        "email": serializers.EmailField(),
    },
)



UserBasicContactInfoSchema = inline_serializer(
    name="UserBasicContactInfo",
    fields={
        "phone": serializers.CharField(),
        "address": serializers.CharField(),
        "emergency_contact": serializers.CharField(),
    }
)