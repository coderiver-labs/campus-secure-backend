
from django.db import models

from rest_framework import serializers

# import models
from accounts.models import CustomUser, StudentProfile

# import utils
from utils.serializers import READ_ONLY_FIELDS



# create serializers


from accounts.serializers import get_user_basic_info

class StudentProfileSerializer(serializers.ModelSerializer):
    user = serializers.SerializerMethodField()

    class Meta:
        model = StudentProfile
        fields = "__all__"
        read_only_fields = ["user"] + READ_ONLY_FIELDS

    def get_user(self, obj: StudentProfile):
        return get_user_basic_info(user=obj.user)
    
    # def to_representation(self, instance):
    #     data = super().to_representation(instance)
    #     data["user"] = get_user_basic_info(user=instance.user)
    #     return data


    



