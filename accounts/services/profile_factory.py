
# DRF
from rest_framework.request import HttpRequest

# import exception

from accounts.exceptions import ProfileCreationError

# import models 
from accounts.models import CustomUser, StudentProfile, StudentAcademicInfo, StudentParentsInfo, StudentContactInfo, StudentHealthInfo
from accounts.models import TeacherContactInfo, TeacherProfile, TeacherProfessionalInfo
from accounts.models import StaffProfile, AdminProfile, AdminContactInfo, StaffContactInfo

# import audit
from audit.services import AuditService


# create profile factory


def create_student_profile(user: CustomUser, request: HttpRequest):
    profile = StudentProfile.objects.create(user=user)
    academic = StudentAcademicInfo.objects.create(student=profile)
    parents = StudentParentsInfo.objects.create(student=profile)
    contact = StudentContactInfo.objects.create(student=profile)
    health = StudentHealthInfo.objects.create(student=profile)

    items = [
        (profile, "Student Profile Created"),
        (academic, "Student Academic Info Created"),
        (parents, "Student Parents Info Created"),
        (contact, "Student Contact Info Created"),
        (health, "Student Health Info Created"),
    ]

    for instance, desc in items:
        AuditService.create_log(actor=request.user, instance=instance, request=request, description=desc)

    return profile


def create_teacher_profile(user: CustomUser, request: HttpRequest):
    profile = TeacherProfile.objects.create(user=user)
    contact = TeacherContactInfo.objects.create(teacher=profile)
    pro_info = TeacherProfessionalInfo.objects.create(teacher=profile)
    
    items = [
        (profile, "Teacher Profile Created"),
        (contact, "Teacher Contact Info Created"),
        (pro_info, "Teacher Professional Info Created"),
    ]

    for instance, desc in items:
        AuditService.create_log(actor=request.user, instance=instance, request=request, description=desc)

    return profile


def create_staff_profile(user: CustomUser, request: HttpRequest):
    profile = StaffProfile.objects.create(user=user)
    contact = StaffContactInfo.objects.create(staff=profile)

    items = [
        (profile, "Staff Profile Created"),
        (contact, "Staff Contact Info Created")
    ]
    for instance , desc in items:
        AuditService.create_log(actor=request.user, instance=instance, request=request, description=desc)

    return profile


def create_admin_profile(user: CustomUser, request: HttpRequest):
    profile = AdminProfile.objects.create(user=user)
    contact = AdminContactInfo.objects.create(admin=profile)
    
    items = [
        (profile, "Admin Profile Created"),
        (contact, "Admin Contact Info Created")
    ]
    
    for instance , desc in items:
        AuditService.create_log(actor=request.user, instance=instance, request=request, description=desc)

    return profile


class ProfileFactory:

    REGISTRY = {
        "student": create_student_profile,
        "teacher": create_teacher_profile,
        "staff": create_staff_profile,
        "admin": create_admin_profile,
    }

    @classmethod
    def create(cls, user: CustomUser, request: HttpRequest):
        creator = cls.REGISTRY.get(user.role)

        if not creator:
            raise ProfileCreationError(
                f"Unsupported role: {user.role}"
            )

        return creator(user=user, request=request)