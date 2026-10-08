import code
from rest_framework import serializers
from django.contrib.auth.hashers import check_password
from django.contrib.auth import authenticate

# import models 
from accounts.base_model import BaseContactInfo
from accounts.models import (
    CustomUser, 
    StudentAcademicInfo, 
    StudentProfile, 
    StudentContactInfo, 
    StudentParentsInfo, 
    StudentHealthInfo,
)
from accounts.models import StaffProfile, StaffPosition, StaffContactInfo
from accounts.models import AdminProfile, AdminContactInfo
from accounts.models import TeacherProfile, TeacherAssignment, TeacherProfessionalInfo, TeacherContactInfo
from school.models import StudentClass

# schema
from accounts.schema import UserBasicInfoSchema

# IMPORT UTILS
from utils.serializers import READ_ONLY_FIELDS

from drf_spectacular.utils import extend_schema_field


# Create Serializer Hare




def get_user_basic_info(*, user: CustomUser) -> dict:
    return {
        "uuid": user.uuid,
        "first_name": user.first_name,
        "last_name": user.last_name,
        "email": user.email,
    }

def get_contact_basic_info(*, contact: BaseContactInfo) -> dict:
    return {
        "phone": contact.phone,
        "address": contact.address,
        "emergency_contact": contact.emergency_contact
    }


class DummySerializer(serializers.Serializer):
    pass

# dummy for swagger
class ProfileSerializer(serializers.Serializer):
    uuid = serializers.UUIDField(allow_null=True)
    position = serializers.CharField(required=False)


# dummy for swagger
class GetAccessTokenResponseSerializer(serializers.Serializer):
    message = serializers.CharField()


# login api serializer
class LoginUserSerializer(serializers.Serializer):
    """
    Simple login serializer — email normalized here as well.
    """

    email = serializers.EmailField(max_length=155)
    password = serializers.CharField(write_only=True, min_length=8, max_length=128)

    def validate_email(self, value: str) -> str:
        return value.strip().lower()

    def validate(self, attrs):
        email = attrs.get("email")
        password = attrs.get("password")
        user = authenticate(email=email, password=password)
        if not user:
            raise serializers.ValidationError({"error": "Invalid email or password"})
        attrs["user"] = user
        return attrs



# resend verify email serializer
class ResendVerifyEmailSerializer(serializers.Serializer):
    email = serializers.EmailField()

    def validate(self, attrs):
        email = attrs.get("email")
        # user = CustomUser.objects.get(email=email)
        try:
            user = CustomUser.objects.get(email=email)
        except CustomUser.DoesNotExist:
            raise serializers.ValidationError({"user": "user does't exist"})
        
        attrs["user"] = user
        return attrs



# reset password serializer
class ResetPasswordSerializer(serializers.Serializer):
    password = serializers.CharField(min_length=7, max_length=15)

    def validate(self, attrs):
        from accounts.helpers import check_prevues_password

        user = self.context.get("user")
        password = attrs.get("password")
        check_prevues_password(old_password=user.password, new_password=password)
        return attrs



class ChangePasswordSerializer(serializers.Serializer):
    old_password = serializers.CharField(min_length=7, max_length=15)
    new_password = serializers.CharField(min_length=7, max_length=15)

    def validate(self, attrs):
        from accounts.helpers import check_prevues_password

        user = self.context.get("user")
        old_password = attrs.get("old_password")
        new_password = attrs.get("new_password")

        if not check_password(old_password, user.password):
            raise serializers.ValidationError(
                {"old_password": "Old password is incorrect."}
            )
        check_prevues_password(old_password=user.password, new_password=new_password)
        return attrs


"""------------User management serializer------------"""
# POST
class CustomUserCreateSerializer(serializers.ModelSerializer):
    position = serializers.SlugRelatedField(slug_field="name", queryset=StaffPosition.objects.all(), required=False)
    student_class = serializers.SlugRelatedField(slug_field="uuid", queryset=StudentClass.objects.all(), required=False)

    class Meta:
        model = CustomUser
        fields = ["uuid", "first_name", "last_name", "email", "role", "student_class", "position", "password"]
        read_only_fields = ["uuid"]
        extra_kwargs = {"password": {"write_only": True, "min_length": 5, "max_length": 15}}

    def validate_role(self, value):
        if value not in dict(CustomUser.CHOICE):
            raise serializers.ValidationError("Invalid role.")
        return value
    

    def validate(self, attrs:dict):
        role = attrs.get("role")
        student_class = attrs.get("student_class")
        position = attrs.get("position")

        if role == "student" and not student_class:
            raise serializers.ValidationError({"student_class": "Student must have a class."})

        if role == "staff" and not position:
            raise serializers.ValidationError({"position": "Staff must have a position."})

        return attrs


# GET Request CustomUser Serializer 
class CustomUserForStaffViewSerializer(serializers.ModelSerializer):
    profile = serializers.SerializerMethodField()
    class Meta:
        model = CustomUser
        exclude = ["password", "groups", "user_permissions", "is_superuser", "is_staff", "last_login"]

    def get_profile(self, obj: CustomUser):
        if obj.role == "student":
            return {"uuid": obj.student_profile.uuid}
        if obj.role == "teacher":
            return {"uuid": obj.teacher_profile.uuid}
        if obj.role == "staff":
            return {"uuid": obj.staff_profile.uuid, "position": obj.staff_profile.position.name}

class CustomUserForSuperUserAndAdminViewSerializer(serializers.ModelSerializer):
    profile = serializers.SerializerMethodField()
    class Meta:
        model = CustomUser
        exclude = ["password", "groups", "user_permissions", "is_superuser", "is_staff"]

    def get_profile(self, obj: CustomUser):
        if obj.role == "student":
            return {"uuid": obj.student_profile.uuid}
        if obj.role == "teacher":
            return {"uuid": obj.teacher_profile.uuid}
        if obj.role == "staff":
            return {"uuid": obj.staff_profile.uuid, "position": obj.staff_profile.position.name}
        if obj.role == "admin" and obj.is_superuser:
            return {"uuid": None}
        if obj.role == "admin":
            return {"uuid": obj.admin_profile.uuid}

from drf_spectacular.utils import extend_schema_field, inline_serializer
class CustomUserForTeacherViewSerializer(serializers.ModelSerializer):
    profile = serializers.SerializerMethodField()
    class Meta:
        model = CustomUser
        fields = ["uuid", "first_name", "last_name", "email", "profile", "role", "is_verified"]
        
    @extend_schema_field(
        inline_serializer(
            name="TeacherStudentProfileResponse",
            fields={"uuid": serializers.UUIDField()}
        )
    )
    def get_profile(self, obj: CustomUser):
        print(obj.role)
        if obj.role == "student":
            return {"uuid": obj.student_profile.uuid}
        

class CustomUserForStudentViewSerializer(serializers.ModelSerializer):
    profile = serializers.SerializerMethodField()
    class Meta:
        model = CustomUser
        exclude = ["password", "groups", "user_permissions", "is_superuser", "is_staff"]

    @extend_schema_field(
        inline_serializer(
            name="StudentProfileResponse",
            fields={"uuid": serializers.UUIDField()}
        )
    )
    def get_profile(self, obj: CustomUser):
        if obj.role == "student":
            return {"uuid": obj.student_profile.uuid}

        

# PUT, PATCH
class CustomUserUpdateSerializer(serializers.ModelSerializer):

    class Meta:
        model = CustomUser
        fields = ["first_name", "last_name","is_active", "is_verified"]



"""_____________________Teacher Assignment serializer_________________"""
# List, Retrieve
class TeacherAssignmentListRetrieveSerializer(serializers.ModelSerializer):
    teacher = serializers.SerializerMethodField()
    student_class = serializers.SerializerMethodField()
    subject = serializers.SerializerMethodField()

    class Meta:
        model = TeacherAssignment
        fields = ["uuid", "teacher", "student_class", "subject"]

    def get_teacher(self, obj: TeacherAssignment):
        return {
            "uuid": obj.teacher.uuid,
            "full_name": obj.teacher.user.get_full_name()
        }

    def get_student_class(self, obj: TeacherAssignment):
        return {
            "uuid": obj.student_class.uuid,
            "class_level": obj.student_class.student_class_level.name,
            "section": obj.student_class.section.section
        }
    
    def get_subject(self, obj: TeacherAssignment):
        return {
            "uuid": obj.subject.uuid,
            "name": obj.subject.name,
            "code": obj.subject.code
        }


# create, update
class TeacherAssignmentCreateUpdateSerializer(serializers.ModelSerializer):
    class Meta:
        model = TeacherAssignment
        fields = ["teacher", "student_class", "subject"]




# ORG
"""___________________Self Profile Serializers Set______________________"""

class StudentProfileSerializer(serializers.ModelSerializer):
    user = serializers.SerializerMethodField()
    academic_info = serializers.SerializerMethodField()
    contact_info = serializers.SerializerMethodField()
    health_info = serializers.SerializerMethodField()
    parents_info = serializers.SerializerMethodField()
    class Meta:
        model = StudentProfile
        exclude = ["created_at", "updated_at"]

    @extend_schema_field(UserBasicInfoSchema)
    def get_user(self, obj: StudentProfile):
        return get_user_basic_info(user=obj.user)

    def get_academic_info(self, obj: StudentProfile):
        academic: StudentAcademicInfo = obj.academic_info
        student_class = academic.student_class
        return {
            "uuid": academic.uuid, 
            "academic_year": f"{academic.start_year}-{academic.end_year}",
            "student_class": (student_class.student_class_level.name if student_class else None,
        ),
            "roll_number": academic.roll_number,
            "admission_date": academic.admission_date
        }
    
    def get_contact_info(self, obj: StudentProfile):
        contact_info: StudentContactInfo = obj.contact_info
        return get_contact_basic_info(contact=contact_info)
    
    def get_health_info(self, obj: StudentProfile):
        health_info: StudentHealthInfo = obj.health_info
        return {
            "blood_group": health_info.blood_group,
            "medical_conditions": health_info.medical_conditions
        }

    def get_parents_info(self, obj: StudentProfile):
        print("serializer")
        parents_info: StudentParentsInfo = obj.parents_info
        return {
            "father_name": parents_info.father_name,
            "father_phone": parents_info.father_phone,
            "mother_name": parents_info.mother_name,
            "mother_phone": parents_info.mother_phone
        }

class TeacherProfileSerializer(serializers.ModelSerializer):
    teacher = serializers.SerializerMethodField()
    assignments = serializers.SerializerMethodField()
    professional_info = serializers.SerializerMethodField()
    contact_info = serializers.SerializerMethodField()

    class Meta:
        model = TeacherProfile
        exclude = ["created_at", "updated_at"]

    def get_teacher(self, obj: TeacherProfile):
        user: CustomUser = obj.user
        return get_user_basic_info(user=user)

    def get_assignments(self, obj: TeacherProfile):
        assignments = obj.assignments.all()
        return [
            {
                "student_class": {"class_level": assignment.student_class.student_class_level.name,},
                "subject": {"name": assignment.subject.name,},
            } for assignment in assignments
        ]

    def get_professional_info(self, obj: TeacherProfile):
        professional_info: TeacherProfessionalInfo = obj.professional_info
        return {
            "qualification": professional_info.qualification,
            "years_of_experience": professional_info.years_of_experience,
            "subjects_specialization": professional_info.subjects_specialization,
            "education_qualification": professional_info.education_qualification
        }

    def get_contact_info(self, obj: TeacherProfile):
        contact_info: TeacherContactInfo = obj.contact_info 
        return get_contact_basic_info(contact=contact_info)
     
class StaffProfileSerializer(serializers.ModelSerializer):
    user = serializers.SerializerMethodField()
    position = serializers.SerializerMethodField()
    contact_info = serializers.SerializerMethodField()
    class Meta:
        model = StaffProfile
        exclude = ["created_at", "updated_at"]

    @extend_schema_field(UserBasicInfoSchema)
    def get_user(self, obj: StaffProfile):
        return get_user_basic_info(user=obj.user)
    
    def get_position(self, obj: StaffProfile):
        return {"name": obj.position.name}
    
    def get_contact_info(self, obj: StaffProfile):
        contact_info: StaffContactInfo = obj.contact_info
        return get_contact_basic_info(contact=contact_info)

class AdminProfileSerializer(serializers.ModelSerializer):
    user = serializers.SerializerMethodField()
    contact_info = serializers.SerializerMethodField()
    class Meta:
        model = AdminProfile
        exclude = ["created_at", "updated_at"]

    @extend_schema_field(UserBasicInfoSchema)
    def get_user(self, obj: AdminProfile):
        return get_user_basic_info(user=obj.user)

    def get_contact_info(self, obj: AdminProfile):
        contact_info: AdminContactInfo = obj.contact_info
        return get_contact_basic_info(contact=contact_info)
    





"""____________Student Related Info_____________"""

# GET
class StudentAcademicInfoGETSerializer(serializers.ModelSerializer):
    student = serializers.SerializerMethodField()
    student_class = serializers.SerializerMethodField()
    class Meta:
        model = StudentAcademicInfo
        fields = "__all__"
        read_only_fields = READ_ONLY_FIELDS
    
    def get_student(self, obj: StudentAcademicInfo):
        return {
            "student_uuid": obj.student_id,
            **get_user_basic_info(user=obj.student.user)

        }
    
    def get_student_class(self, obj: StudentAcademicInfo):
        if getattr(obj, "student_class"):
            return {
                "uuid": obj.student_class.uuid,
                "class_level": obj.student_class.student_class_level.name
            }
        # return None
    
class StudentAcademicInfoUpdateSerializer(serializers.ModelSerializer):
    class Meta:
        model = StudentAcademicInfo
        fields = "__all__"
        read_only_fields = ["student"] + READ_ONLY_FIELDS
    
    def to_representation(self, instance):
        return super().to_representation(instance) # ata ke overwrite korte hobe, GET serializer diye response dibo
   
        
# GET
class StudentContactInfoGetSerializer(serializers.ModelSerializer):
    student = serializers.SerializerMethodField()
    class Meta:    
        model = StudentContactInfo
        fields = "__all__" 

    def get_student(self, obj: StudentContactInfo):
        return {
            "student_id": obj.student_id,
            **get_user_basic_info(user=obj.student.user)
        }

# UPDATE
class StudentContactInfoUpdateSerializer(serializers.ModelSerializer):
    class Meta:
        model = StudentContactInfo
        fields = "__all__"   
        read_only_fields = ["student", ] + READ_ONLY_FIELDS



# GET
class StudentHealthInfoGetSerializer(serializers.ModelSerializer):
    student = serializers.SerializerMethodField()
    class Meta:    
        model = StudentHealthInfo
        fields = "__all__" 

    def get_student(self, obj: StudentParentsInfo):
        return {
            "student_id": obj.student_id,
            **get_user_basic_info(user=obj.student.user)
        }
    
# UPDATE
class StudentHealthInfoUpdateSerializer(serializers.ModelSerializer):
    class Meta:
        model = StudentParentsInfo
        fields = "__all__"   
        read_only_fields = ["student", ] + READ_ONLY_FIELDS



# GET
class StudentParentsInfoGetSerializer(serializers.ModelSerializer):
    student = serializers.SerializerMethodField()
    class Meta:    
        model = StudentParentsInfo
        fields = "__all__" 

    def get_student(self, obj: StudentParentsInfo):
        return {
            "student_id": obj.student_id,
            **get_user_basic_info(user=obj.student.user)
        }

# UPDATE
class StudentParentsInfoUpdateSerializer(serializers.ModelSerializer):
    class Meta:
        model = StudentParentsInfo
        fields = "__all__"   
        read_only_fields = ["student", ] + READ_ONLY_FIELDS




"""_________________Teacher Related  Info___________________"""
# GET
class TeacherContactInfoGetSerializer(serializers.ModelSerializer):
    teacher = serializers.SerializerMethodField()
    class Meta:
        model = TeacherContactInfo
        fields = "__all__"

    def get_teacher(self, obj: TeacherContactInfo):
        return {
            "teacher_id": obj.teacher.uuid,
            **get_user_basic_info(user=obj.teacher.user)
        }

# UPDATE
class TeacherContactInfoUpdateSerializer(serializers.ModelSerializer):
    class Meta:
        model = TeacherContactInfo
        fields = "__all__"
        read_only_fields = ["teacher"] + READ_ONLY_FIELDS


# GET
class TeacherProfessionalInfoGetSerializer(serializers.ModelSerializer):
    teacher = serializers.SerializerMethodField()
    class Meta:
        model = TeacherProfessionalInfo
        fields = "__all__"

    def get_teacher(self, obj: TeacherContactInfo):
        return {
            "teacher_id": obj.teacher.uuid,
            **get_user_basic_info(user=obj.teacher.user)
        }
    
# UPDATE
class TeacherProfessionalInfoUpdateSerializer(serializers.ModelSerializer):
    class Meta:
        model = TeacherContactInfo
        fields = "__all__"
        read_only_fields = ["teacher"] + READ_ONLY_FIELDS



"""________________Staff Related Serializer___________________"""
from accounts.models import StaffPosition
"""Admin Only Serializer"""
## GET & POST
class StaffPositionSerializer(serializers.ModelSerializer):
    class Meta:
        model = StaffPosition
        fields = "__all__"
        read_only_fields = READ_ONLY_FIELDS



# GET
class StaffContactInfoGetSerializer(serializers.ModelSerializer):
    class Meta:
        model = StaffContactInfo
        fields = "__all__"

# UPDATE
class StaffContactInfoUpdateSerializer(serializers.ModelSerializer):
    class Meta:
        model = StaffContactInfo
        fields = "__all__"
        read_only_fields = ["staff"] + READ_ONLY_FIELDS




"""________________Admin Related Serializer___________________"""
from accounts.models import AdminContactInfo
# GET
class AdminContactInfoGetSerializer(serializers.ModelSerializer):
    class Meta:
        model = AdminContactInfo
        fields = "__all__"

# UPDATE
class AdminContactInfoUpdateSerializer(serializers.ModelSerializer):
    class Meta:
        model = AdminContactInfo
        fields = "__all__"
        read_only_fields = ["admin"] + READ_ONLY_FIELDS

