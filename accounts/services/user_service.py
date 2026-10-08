from django.db import transaction
from accounts.services.profile_factory import ProfileFactory

# DRF
from rest_framework.request import HttpRequest

# import models
from accounts.models import CustomUser
from accounts.models import StudentProfile, StaffProfile, AdminProfile

# import celery task
from celery_task.task import celery_send_verify_mail

# import audit 
from audit.services import AuditService

# create user services

    
class UserCreationService:

    @staticmethod
    @transaction.atomic
    def execute(*, validated_data: dict, request: HttpRequest) -> CustomUser:
        data = validated_data.copy()
        position = data.pop("position", None)
        student_class = data.pop("student_class", None)

        user: CustomUser = CustomUser.objects.create_user(**data)

        # Superuser does not get profile
        if user.is_superuser:
            return user

        profile = ProfileFactory.create(user=user, request=request)

        if user.role == "staff" and position:
            profile: StaffProfile = profile
            profile.position = position
            profile.save(update_fields=["position"])

        if user.role == "student" and student_class:
            profile: StudentProfile = profile
            profile.academic_info.student_class = student_class
            profile.academic_info.save(update_fields=["student_class"])


        AuditService.create_log(
            actor=request.user,
            instance=user,
            request=request,
            description="Create user"
        )
        
        transaction.on_commit(
            lambda: celery_send_verify_mail.delay(
                user.uuid, purpose="verify_email"
            )
        )

        return user