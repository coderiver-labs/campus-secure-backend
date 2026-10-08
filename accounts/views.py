from accounts.models import CustomUser
from django.db import transaction

# import Rest Framework
from rest_framework.generics import GenericAPIView
from rest_framework.response import Response
from rest_framework import status

# import serializers
from rest_framework.serializers import Serializer
from utils.serializers import DummySerializer
from accounts.serializers import ResendVerifyEmailSerializer
from accounts.serializers import ResetPasswordSerializer
from accounts.serializers import LoginUserSerializer
from accounts.serializers import CustomUserCreateSerializer, CustomUserForSuperUserAndAdminViewSerializer, CustomUserUpdateSerializer

# import authentication
from auth.cookies import CookieHandler, AuthCookieService
from auth.validators import validate_refresh_token, verify_one_time_token

# invariant permission
from permission.policy.role_policy import RolePolicyPermission
from permission.rules.superuser import SuperuserProtectionPermission
from permission.rules.admin import AdminSelfProtectionPermission
from permission.rules.staff import StaffBoundaryPermission

# final permission
from permission.domain.user import UserDomainPermission


# import services
from accounts.services.user_service import UserCreationService

# import utils
from utils.public_base_APIView import PublicGenericAPIView
from accounts.base_views import BaseUserManagementView

# import helper
from accounts.helpers import verify_user

# import mixin utils
from utils.mixins import CSRFCookieMixin

# celery tasks
from celery_task.task import celery_verify_success_mail
from celery_task.task import celery_send_verify_mail
from celery_task.task import celery_send_reset_password_mail
from celery_task.task import celery_password_reset_success_mail

# python
from typing import cast

# import Docs
from drf_spectacular.utils import extend_schema, extend_schema_view

# import logging
import logging
logger = logging.getLogger(__name__)

# audit log
from audit.services import AuditService








# Create your views here.



"""Spectacular APIView"""
from drf_spectacular.views import SpectacularAPIView, SpectacularRedocView, SpectacularSwaggerView
from rest_framework.permissions import AllowAny


class PublicSchemaView(SpectacularAPIView):
    permission_classes = [AllowAny]
    authentication_classes = []
    
class PublicRedocView(SpectacularRedocView):
    permission_classes = [AllowAny]
    authentication_classes = []
    
class PublicSwaggerView(SpectacularSwaggerView):
    permission_classes = [AllowAny]
    authentication_classes = []





"""______________________Authentication, Validation And Passwd Management________________"""
@extend_schema(tags=["Authentication"])
class GetCSRFToken(CSRFCookieMixin, PublicGenericAPIView):
    """
    GetCsrfToken is a public API for retrieving a CSRF token.

    - This API uses a **GET request**
    - When you call this API, a **CSRF token will be automatically set in your browser cookie**
    - The CSRF token is required for all unsafe requests such as **POST, PUT, PATCH, DELETE**
    - This improves security and prevents Cross-Site Request Forgery (CSRF) attacks
    - Rate Limit: Maximum 10 requests per minute per IP
    """

    serializer_class = DummySerializer
    
    def get(self, request, *args, **kwargs):
        logger.info(
            "CSRF token retrieved successfully",
            extra={
                "action": "get_csrf_token",
            }
        )
        return Response(status=status.HTTP_200_OK)



@extend_schema(tags=["Authentication"])
class VerifyAccountAPI(PublicGenericAPIView):
    """
    VerifyAccountAPI is a public API for verifying user accounts.
    - This API uses a **GET request**
    - The `token` parameter in the URL is a one-time token sent to the user's email for account verification.
    - On successful verification, the user's account will be marked as verified.
    """

    def get(self, request, token):
        from celery.app.task import Task

        user: CustomUser = verify_one_time_token(signed_token=token, purpose="verify_email")
        verify_user(user=user)
        task = cast(Task, celery_verify_success_mail)
        task.delay(user_uuid=str(user.uuid))
        return Response({"verify": "account verify successfully"})

@extend_schema(tags=["Authentication"])
class ResendVerificationEmailAPI(PublicGenericAPIView):
    """
    ResendVerificationEmailAPI is a public API for resending account verification emails.
    - This API uses a **POST request**
    - Required field: `email`
    - If the user is not already verified, a new verification email will be sent to the provided email address.
    - Rate Limit: Maximum 10 requests per minute per IP
    """

    serializer_class = ResendVerifyEmailSerializer

    def post(self, request):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        user = serializer.validated_data.get("user")
        if user.is_verified:
            return Response({"message": "User has been verified"}, status=status.HTTP_200_OK)
        celery_send_verify_mail.delay(user_uuid=str(user.uuid), purpose="verify_email")
        return Response({"message": "Verify mail send successfully"}, status=status.HTTP_200_OK)

@extend_schema(
    tags=["Authentication"],
)
class ForgetPasswordAPI(PublicGenericAPIView):
    """
    ForgetPasswordAPI is a public API for initiating the password reset process.
    - This API uses a **POST request**
    - Required field: `email`
    - If the user exists, a password reset email will be sent to the provided email address.
    - Rate Limit: Maximum 5 requests per minute per IP
    """

    serializer_class = ResendVerifyEmailSerializer

    def post(self, request):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        user = serializer.validated_data.get("user")
        celery_send_reset_password_mail.delay(
            user_uuid=str(user.uuid), purpose="reset_password"
        )
        return Response({"message": "check your mail , amd reset your password"})

from accounts.helpers import update_token_password
@extend_schema(
    tags=["Authentication"],
)
class ResetPasswordAPI(PublicGenericAPIView):
    """
    ResetPasswordAPI is a public API for resetting user passwords.
    - This API uses a **POST request**
    - Required field: `password`
    - On successful password reset, the user's password will be updated.
    """

    serializer_class = ResetPasswordSerializer

    def post(self, request, token):
        user = verify_one_time_token(signed_token=token, purpose="reset_password")
        serializer = self.get_serializer(data=request.data, context={"user": user})
        serializer.is_valid(raise_exception=True)
        password = serializer.validated_data.get("password")
        update_token_password(user=user, password=password)
        celery_password_reset_success_mail.delay(user_uuid=str(user.uuid))
        return Response(
            {"message": "password update successfully"}, status=status.HTTP_200_OK
        )


from accounts.serializers import ChangePasswordSerializer
@extend_schema(tags=["Authentication"])
class ChangePasswordAPI(GenericAPIView):
    """
    ChangePasswordAPI is a protected API for changing user passwords.
    - This API uses a **POST request**
    - Required fields: `old_password`, `new_password`
    - On successful password change, the user's password will be updated.
    """

    serializer_class = ChangePasswordSerializer

    def post(self, request):
        user: CustomUser = request.user
        serializer = self.get_serializer(data=request.data, context={"user": user})
        serializer.is_valid(raise_exception=True)
        new_password = serializer.validated_data.get("new_password")
        update_token_password(user=user, password=new_password)
        celery_password_reset_success_mail.delay(user_uuid=str(user.uuid))
        return Response(
            {"message": "password change successfully"}, status=status.HTTP_200_OK
        )





"""___________________Authentication APIs___________________"""
from drf_spectacular.utils import extend_schema
@extend_schema(
    tags=["Authentication"],
)
class LoginGenericAPIView(PublicGenericAPIView):
    """
    LoginGenericAPIView is a public API for user login.
    - This API uses a **POST request**
    - Required fields: `email`, `password`
    - On successful login, authentication cookies will be set in the response.
    - Rate Limit: Maximum 5 login attempts per minute per IP
    """
    # throttle_classes = [LoginThrottle]
    throttle_scope = "login"
    serializer_class = LoginUserSerializer

    def post(self, request):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        user = serializer.validated_data.get("user")
        response = Response({"message": "Login successfully"}, status=status.HTTP_200_OK)
        cookie = AuthCookieService(request=request, user=user)
        response = cookie.set_login_cookies(response=response)

        logger.info(
            "User Login Successfully",
            extra={
                "action": "get_csrf_token",
            }
        )
        
        return response
from accounts.serializers import GetAccessTokenResponseSerializer


@extend_schema(
    tags=["Authentication"],
    request=None,
    responses={
        200: GetAccessTokenResponseSerializer,
    },
)
class GetAccessTOkenAPI(PublicGenericAPIView):
    """
    Issue a new access token from a valid refresh token and set it as a secure cookie.

    - Purpose: validate an incoming refresh token, generate a new access token,
      and attach that access token to the response as an HTTP-only secure cookie.
      can easily follow the flow and understand CookieHandler usage.
    - Behavior:
        * Validates refresh token (via validate_refresh_token).
        * Creates a Response containing a success message or token payload.
        * Uses CookieHandler to set the access token cookie and returns the final response.
    - Authentication: public endpoint that accepts a refresh token (usually sent via cookie).
    - Response: returns the response produced by CookieHandler (cookie set + JSON body).
    """
    def post(self, request):
        token = validate_refresh_token(request=request)
        response = Response({"access_token": "new access token set successfully"})
        cookie = CookieHandler(request=request, response=response)
        cookie.set_access_token(str(token.access_token))
        return cookie.get_response()

@extend_schema(tags=["Authentication"])
class LogoutGenericAPIView(GenericAPIView):
    """
    LogoutAPI is a public API for user logout.
    - This API uses a **POST request**
    - On successful logout, authentication cookies will be cleared from the response.
    - Rate Limit: Maximum 10 requests per minute per IP
    """

    serializer_class = DummySerializer

    def post(self, request):
        response = Response({"message": "Logout successfully"}, status=status.HTTP_200_OK)
        cookie = CookieHandler(request=request, user=request.user, response=response)
        cookie.delete_token()
        return cookie.get_response()






"""___________________________User Management____________________"""

from drf_spectacular.utils import extend_schema_view, extend_schema, PolymorphicProxySerializer
from accounts.serializers import (
    CustomUserForStaffViewSerializer,
    CustomUserForTeacherViewSerializer,
    CustomUserForStudentViewSerializer
)
user_response_serializer = PolymorphicProxySerializer(
    component_name='UserResponseByRole',
    serializers={
        'admin': CustomUserForSuperUserAndAdminViewSerializer,
        'staff': CustomUserForStaffViewSerializer,
        'teacher': CustomUserForTeacherViewSerializer,
        'student': CustomUserForStudentViewSerializer,
    },
    resource_type_field_name=None,
)

@extend_schema_view(
    list=extend_schema(
        summary="List users",
        description=(
            "Retrieve a list of users accessible to the authenticated user. "
            "The returned users are automatically filtered according to the "
            "authenticated user's role and access boundaries.\n\n"
            "Superusers can access all users. Admins can access staff, teachers, "
            "and students, including themselves. Staff can access teachers and "
            "students, including themselves. Teachers can access students who "
            "belong to classes assigned to them. \n\n"
            "Supports filtering, searching, and ordering using the configured "
            "query parameters."
        ),
        responses={200: user_response_serializer},
        tags=["Accounts"],
    ),

    retrieve=extend_schema(
        summary="Retrieve a user",
        description=(
            "Retrieve detailed information about a specific user identified "
            "by their UUID.\n\n"
            "Access to the requested user is determined by the authenticated "
            "user's role and the configured permission policies. The response "
            "contains user information together with the accessible profile "
            "information."
        ),
        responses={200: user_response_serializer},
        tags=["Accounts"],
    ),

    create=extend_schema(
        summary="Create a user",
        description=(
            "Create a new user account with an optional role-specific profile.\n\n"
            "Students must provide a `student_class`. Staff users must provide "
            "a `position`. Teacher and admin profile data are handled by the "
            "user creation service according to the selected role.\n\n"
            "The password is accepted only during creation and is write-only."
        ),
        request=CustomUserCreateSerializer,
        responses={201: CustomUserForSuperUserAndAdminViewSerializer,},
        tags=["Accounts"],
    ),

    update=extend_schema(
        summary="Update a user",
        description=(
            "Replace the allowed user information for an existing user.\n\n"
            "Only the fields exposed by the update serializer can be modified: "
            "`first_name`, `last_name`, `is_active`, and `is_verified`.\n\n"
            "Updating a user's role, email, password, UUID, or profile-specific "
            "fields is not supported by this endpoint."
        ),
        request=CustomUserUpdateSerializer,
        responses={
            200: CustomUserUpdateSerializer,
        },
        tags=["Accounts"],
    ),

    partial_update=extend_schema(
        summary="Partially update a user",
        description=(
            "Partially update an existing user's information.\n\n"
            "Any combination of the supported fields may be provided. "
            "Fields that are not included in the request remain unchanged.\n\n"
            "Supported fields are `first_name`, `last_name`, `is_active`, "
            "and `is_verified`."
        ),
        request=CustomUserUpdateSerializer,
        responses={
            200: CustomUserUpdateSerializer,
        },
        tags=["Accounts"],
    ),

    destroy=extend_schema(
        summary="Delete a user",
        description=(
            "Delete a user account and its associated profile and related "
            "user information according to the configured database "
            "relationships.\n\n"
            "The authenticated user's permissions and role boundaries are "
            "checked before deletion. A deletion audit record is created "
            "before the user is removed."
        ),
        responses={
            204: None,
        },
        tags=["Accounts"],
    ),
)
class UserManagementAPI(BaseUserManagementView):

    permission_classes = [
        RolePolicyPermission,
        SuperuserProtectionPermission,
        AdminSelfProtectionPermission,
        StaffBoundaryPermission,
        UserDomainPermission
    ]

    permission_key = "user"
    lookup_field = "uuid"

    def perform_create(self, serializer: Serializer):
        user = UserCreationService.execute(
            validated_data=serializer.validated_data,
            request=self.request
        )
        serializer.instance = user

        
    def perform_update(self, serializer: Serializer):

        with transaction.atomic():
            instance = self.get_object()

            AuditService.update_log(
                actor=self.request.user,
                instance=instance,
                validated_data=serializer.validated_data,
                request=self.request,
                description="User Update"
            )
            serializer.save() # updated_instance

            
    def perform_destroy(self, instance: CustomUser):
        with transaction.atomic():

            AuditService.delete_log(
                actor=self.request.user,
                instance=instance,
                request=self.request,
                description="user Delete with user_profile, user_contact and all user info"
            )
            instance.delete()
        


from rest_framework.request import Request
from accounts.base_views import BaseProfileAPIView
from accounts.permissions.policy import ProfileAPIViewPolicy
from drf_spectacular.utils import (extend_schema, extend_schema_view, OpenApiResponse)

@extend_schema_view(
    get=extend_schema(
        summary="Retrieve user profile",
        description="Retrieve the profile information of the authenticated user.",
        tags=["Accounts"],
        responses={
            status.HTTP_200_OK: OpenApiResponse(
                description="User profile retrieved successfully."
            ),
        },
    ),
)
class ProfileAPIView(BaseProfileAPIView):
    permission_classes = [ProfileAPIViewPolicy,]

    def get(self, request: Request, *args, **kwargs):
        return self.retrieve(request=request, *args, **kwargs)


from accounts.base_views import BaseTeacherAssignmentViewSet
from accounts.models import TeacherAssignment
from accounts.permissions.policy import TeacherAssignmentPolicy

from rest_framework import status
from drf_spectacular.utils import extend_schema, extend_schema_view

from accounts.serializers import TeacherAssignmentListRetrieveSerializer, TeacherAssignmentCreateUpdateSerializer

@extend_schema_view(
    list=extend_schema(
        summary="List teacher assignments",
        description="Retrieve a list of teacher assignments with filtering, searching, and ordering support.",
        tags=["Teacher Assignments"],
        responses={
            status.HTTP_200_OK: TeacherAssignmentListRetrieveSerializer(many=True),
        },
    ),

    create=extend_schema(
        summary="Create a teacher assignment",
        description="Assign a teacher to a student class and subject.",
        tags=["Teacher Assignments"],
        request=TeacherAssignmentCreateUpdateSerializer,
        responses={
            status.HTTP_201_CREATED: TeacherAssignmentListRetrieveSerializer,
        },
    ),

    retrieve=extend_schema(
        summary="Retrieve a teacher assignment",
        description="Retrieve details of a specific teacher assignment.",
        tags=["Teacher Assignments"],
        responses={
            status.HTTP_200_OK: TeacherAssignmentListRetrieveSerializer,
        },
    ),

    update=extend_schema(
        summary="Update a teacher assignment",
        description="Update an existing teacher assignment.",
        tags=["Teacher Assignments"],
        request=TeacherAssignmentCreateUpdateSerializer,
        responses={
            status.HTTP_200_OK: TeacherAssignmentListRetrieveSerializer,
        },
    ),

    partial_update=extend_schema(
        summary="Partially update a teacher assignment",
        description="Partially update an existing teacher assignment.",
        tags=["Teacher Assignments"],
        request=TeacherAssignmentCreateUpdateSerializer,
        responses={
            status.HTTP_200_OK: TeacherAssignmentListRetrieveSerializer,
        },
    ),

    destroy=extend_schema(
        summary="Delete a teacher assignment",
        description="Delete an existing teacher assignment.",
        tags=["Teacher Assignments"],
        responses={
            status.HTTP_204_NO_CONTENT: None,
        },
    ),
)
class TeacherAssignmentAPI(BaseTeacherAssignmentViewSet):
    
    permission_classes = [
        TeacherAssignmentPolicy,
    ]

    def get_queryset(self):
        policy_class = self.permission_classes[0]
        qs = policy_class.scope_queryset(request=self.request, qs=self.queryset)
        return qs


    def perform_create(self, serializer: Serializer):
        with transaction.atomic():
            instance = serializer.save()
            AuditService.create_log(
                actor=self.request.user,
                instance=instance,
                request=self.request,
                description="Teacher Assignment Create"
            )


    def perform_update(self, serializer: Serializer):
        with transaction.atomic():
            instance = self.get_object()
            AuditService.update_log(
                actor=self.request.user,
                instance=instance,
                validated_data=serializer.validated_data,
                request=self.request,
                description="Teacher Assignment Update",
            )
            serializer.save()

    def perform_destroy(self, instance: TeacherAssignment):
        with transaction.atomic():
            AuditService.delete_log(
                actor=self.request.user,
                instance=instance,
                request=self.request,
                description="Teacher Assignment Deleted"
            )
            instance.delete()








"""_____________________Student Related Info___________________"""
from accounts.permissions.policy import StudentRelatedInfoPolicy
from accounts.base_views import BaseStudentAcademicInfoView, BaseStudentParentsInfoView, BaseStudentContactInfoView, BaseStudentHealthInfoView

from accounts.serializers import StudentAcademicInfoGETSerializer, StudentAcademicInfoUpdateSerializer 
from drf_spectacular.utils import extend_schema, extend_schema_view
from rest_framework import status

from rest_framework import status

@extend_schema_view(
    list=extend_schema(
        summary="List student academic information",
        description="Retrieve academic information of students accessible to the authenticated user.",
        tags=["Student Profile & Academic"],
        responses={
            status.HTTP_200_OK: StudentAcademicInfoGETSerializer(many=True),
        },
    ),
    retrieve=extend_schema(
        summary="Retrieve student academic information",
        description="Retrieve academic information for a specific student.",
        tags=["Student Profile & Academic"],
        responses={
            status.HTTP_200_OK: StudentAcademicInfoGETSerializer,
        },
    ),
    update=extend_schema(
        summary="Update student academic information",
        description="Update the academic information of a student.",
        tags=["Student Additional Information"],
        request=StudentAcademicInfoUpdateSerializer,
        responses={
            status.HTTP_200_OK: StudentAcademicInfoGETSerializer,
        },
    ),
    partial_update=extend_schema(
        summary="Partially update student academic information",
        description="Partially update the academic information of a student.",
        tags=["Student Profile & Academic"],
        request=StudentAcademicInfoUpdateSerializer,
        responses={
            status.HTTP_200_OK: StudentAcademicInfoGETSerializer,
        },
    ),
)
class StudentAcademicInfoView(BaseStudentAcademicInfoView):
    permission_classes = [StudentRelatedInfoPolicy,]

    def perform_update(self, serializer: Serializer):
        with transaction.atomic():
            instance = self.get_object()            

            AuditService.update_log(
                actor=self.request.user,
                instance=instance,
                validated_data=serializer.validated_data,
                request=self.request,
                description="Student Academic Info"
            )
            serializer.save()

from accounts.serializers import StudentParentsInfoGetSerializer, StudentParentsInfoUpdateSerializer
@extend_schema_view(
    list=extend_schema(
        summary="List student parents information",
        description="Retrieve parents information of students accessible to the authenticated user.",
        tags=["Student Additional Information"],
        responses={
            status.HTTP_200_OK: StudentParentsInfoGetSerializer(many=True),
        },
    ),
    retrieve=extend_schema(
        summary="Retrieve student parents information",
        description="Retrieve parents information for a specific student.",
        tags=["Student Additional Information"],
        responses={
            status.HTTP_200_OK: StudentParentsInfoGetSerializer,
        },
    ),
    update=extend_schema(
        summary="Update student parents information",
        description="Update the parents information of a student.",
        tags=["Student Additional Information"],
        request=StudentParentsInfoUpdateSerializer,
        responses={
            status.HTTP_200_OK: StudentParentsInfoGetSerializer,
        },
    ),
    partial_update=extend_schema(
        summary="Partially update student parents information",
        description="Partially update the parents information of a student.",
        tags=["Student Additional Information"],
        request=StudentParentsInfoUpdateSerializer,
        responses={
            status.HTTP_200_OK: StudentParentsInfoGetSerializer,
        },
    ),
)
class StudentParentsInfoView(BaseStudentParentsInfoView):
    permission_classes = [StudentRelatedInfoPolicy]

    def perform_update(self, serializer: Serializer):
        with transaction.atomic():
            instance = self.get_object()            

            AuditService.update_log(
                actor=self.request.user,
                instance=instance,
                validated_data=serializer.validated_data,
                request=self.request,
                description="Student Parents Info Update"
            )
            serializer.save()

from accounts.serializers import StudentContactInfoGetSerializer, StudentContactInfoUpdateSerializer
@extend_schema_view(
    list=extend_schema(
        summary="List student contact information",
        description="Retrieve contact information of students accessible to the authenticated user.",
        tags=["Student Additional Information"],
        responses={
            status.HTTP_200_OK: StudentContactInfoGetSerializer(many=True),
        },
    ),
    retrieve=extend_schema(
        summary="Retrieve student contact information",
        description="Retrieve contact information for a specific student.",
        tags=["Student Additional Information"],
        responses={
            status.HTTP_200_OK: StudentContactInfoGetSerializer,
        },
    ),
    update=extend_schema(
        summary="Update student contact information",
        description="Update the contact information of a student.",
        tags=["Student Additional Information"],
        request=StudentContactInfoUpdateSerializer,
        responses={
            status.HTTP_200_OK: StudentContactInfoGetSerializer,
        },
    ),
    partial_update=extend_schema(
        summary="Partially update student contact information",
        description="Partially update the contact information of a student.",
        tags=["Student Additional Information"],
        request=StudentContactInfoUpdateSerializer,
        responses={
            status.HTTP_200_OK: StudentContactInfoGetSerializer,
        },
    ),
)
class StudentContactInfoView(BaseStudentContactInfoView):
    permission_classes = [StudentRelatedInfoPolicy]

    def perform_update(self, serializer: Serializer):
        with transaction.atomic():
            instance = self.get_object()            

            AuditService.update_log(
                actor=self.request.user,
                instance=instance,
                validated_data=serializer.validated_data,
                request=self.request,
                description="Student Parents Info Update"
            )
            serializer.save()

from accounts.serializers import StudentHealthInfoGetSerializer, StudentHealthInfoUpdateSerializer

@extend_schema_view(
    list=extend_schema(
        summary="List student health information",
        description="Retrieve health information of students accessible to the authenticated user.",
        tags=["Student Additional Information"],
        responses={
            status.HTTP_200_OK: StudentHealthInfoGetSerializer(many=True),
        },
    ),
    retrieve=extend_schema(
        summary="Retrieve student health information",
        description="Retrieve health information for a specific student.",
        tags=["Student Additional Information"],
        responses={
            status.HTTP_200_OK: StudentHealthInfoGetSerializer,
        },
    ),
    update=extend_schema(
        summary="Update student health information",
        description="Update the health information of a student.",
        tags=["Student Additional Information"],
        request=StudentHealthInfoUpdateSerializer,
        responses={
            status.HTTP_200_OK: StudentHealthInfoGetSerializer,
        },
    ),
    partial_update=extend_schema(
        summary="Partially update student health information",
        description="Partially update the health information of a student.",
        tags=["Student Additional Information"],
        request=StudentHealthInfoUpdateSerializer,
        responses={
            status.HTTP_200_OK: StudentHealthInfoGetSerializer,
        },
    ),
)
class StudentHealthInfoView(BaseStudentHealthInfoView):
    permission_classes = [StudentRelatedInfoPolicy,]
    def perform_update(self, serializer: Serializer):
        with transaction.atomic():
            instance = self.get_object()            

            AuditService.update_log(
                actor=self.request.user,
                instance=instance,
                validated_data=serializer.validated_data,
                request=self.request,
                description="Student Health Info Update"
            )
            serializer.save()




"""__________________Teacher Related Info___________________"""
from accounts.permissions.policy import TeacherRelatedViewPolicy
from accounts.base_views import BaseTeacherContactInfoView, BaseTeacherProfessionalInfoView

from accounts.serializers import (
    TeacherContactInfoGetSerializer, 
    TeacherContactInfoUpdateSerializer,
    TeacherProfessionalInfoGetSerializer,
    TeacherProfessionalInfoUpdateSerializer,
    AdminContactInfoUpdateSerializer,
    StaffContactInfoGetSerializer,
    StaffContactInfoUpdateSerializer,
    AdminContactInfoGetSerializer,
    StaffPositionSerializer,
    
)
@extend_schema_view(
    list=extend_schema(
        summary="List teacher contact information",
        description="Retrieve contact information of teachers accessible to the authenticated user.",
        tags=["Teacher Related"],
        responses={
            status.HTTP_200_OK: TeacherContactInfoGetSerializer(many=True),
        },
    ),
    retrieve=extend_schema(
        summary="Retrieve teacher contact information",
        description="Retrieve contact information for a specific teacher.",
        tags=["Teacher Related"],
        responses={
            status.HTTP_200_OK: TeacherContactInfoGetSerializer,
        },
    ),
    update=extend_schema(
        summary="Update teacher contact information",
        description="Update the contact information of a teacher.",
        tags=["Teacher Related"],
        request=TeacherContactInfoUpdateSerializer,
        responses={
            status.HTTP_200_OK: TeacherContactInfoGetSerializer,
        },
    ),
    partial_update=extend_schema(
        summary="Partially update teacher contact information",
        description="Partially update the contact information of a teacher.",
        tags=["Teacher Related"],
        request=TeacherContactInfoUpdateSerializer,
        responses={
            status.HTTP_200_OK: TeacherContactInfoGetSerializer,
        },
    ),
)
class TeacherContactInfoView(BaseTeacherContactInfoView):
    permission_classes = [TeacherRelatedViewPolicy]
    def perform_update(self, serializer: Serializer):
        with transaction.atomic():
            instance = self.get_object()            

            AuditService.update_log(
                actor=self.request.user,
                instance=instance,
                validated_data=serializer.validated_data,
                request=self.request,
                description="Teacher Contact Info Update"
            )
            serializer.save()



@extend_schema_view(
    list=extend_schema(
        summary="List teacher professional information",
        description="Retrieve professional information of teachers accessible to the authenticated user.",
        tags=["Teacher Related"],
        responses={
            status.HTTP_200_OK: TeacherProfessionalInfoGetSerializer(many=True),
        },
    ),
    retrieve=extend_schema(
        summary="Retrieve teacher professional information",
        description="Retrieve professional information for a specific teacher.",
        tags=["Teacher Related"],
        responses={
            status.HTTP_200_OK: TeacherProfessionalInfoGetSerializer,
        },
    ),
    update=extend_schema(
        summary="Update teacher professional information",
        description="Update the professional information of a teacher.",
        tags=["Teacher Related"],
        request=TeacherProfessionalInfoUpdateSerializer,
        responses={
            status.HTTP_200_OK: TeacherProfessionalInfoGetSerializer,
        },
    ),
    partial_update=extend_schema(
        summary="Partially update teacher professional information",
        description="Partially update the professional information of a teacher.",
        tags=["Teacher Related"],
        request=TeacherProfessionalInfoUpdateSerializer,
        responses={
            status.HTTP_200_OK: TeacherProfessionalInfoGetSerializer,
        },
    ),
)
class TeacherProfessionalInfoView(BaseTeacherProfessionalInfoView):
    permission_classes = [TeacherRelatedViewPolicy]
    def perform_update(self, serializer: Serializer):
        with transaction.atomic():
            instance = self.get_object()            

            AuditService.update_log(
                actor=self.request.user,
                instance=instance,
                validated_data=serializer.validated_data,
                request=self.request,
                description="Teacher Professional Info Update"
            )
            serializer.save()



"""_________________Staff Related Info__________________"""
from accounts.base_views import BaseStaffPositionView, BaseStaffContactInfoView
from accounts.permissions.policy import StaffPositionViewPolicy, StaffContactInfoViewPolicy
@extend_schema_view(
    list=extend_schema(
        summary="List staff positions",
        description="Retrieve all available staff positions.",
        tags=["Staff Related"],
        responses={
            status.HTTP_200_OK: StaffPositionSerializer(many=True),
        },
    ),
    retrieve=extend_schema(
        summary="Retrieve a staff position",
        description="Retrieve details of a specific staff position.",
        tags=["Staff Related"],
        responses={
            status.HTTP_200_OK: StaffPositionSerializer,
        },
    ),
    create=extend_schema(
        summary="Create a staff position",
        description="Create a new staff position.",
        tags=["Staff Related"],
        request=StaffPositionSerializer,
        responses={
            status.HTTP_201_CREATED: StaffPositionSerializer,
        },
    ),
)
class StaffPositionView(BaseStaffPositionView):
    permission_classes = [StaffPositionViewPolicy,]

    def perform_create(self, serializer: Serializer):
        with transaction.atomic():

            instance = serializer.save()
            AuditService.create_log(
                actor=self.request.user,
                instance=instance,
                request=self.request,
                description="Staff Position Created"
            )




@extend_schema_view(
    list=extend_schema(
        summary="List staff contact information",
        description="Retrieve contact information of staff members accessible to the authenticated user.",
        tags=["Staff Related"],
        responses={
            status.HTTP_200_OK: StaffContactInfoGetSerializer(many=True),
        },
    ),
    retrieve=extend_schema(
        summary="Retrieve staff contact information",
        description="Retrieve contact information for a specific staff member.",
        tags=["Staff Related"],
        responses={
            status.HTTP_200_OK: StaffContactInfoGetSerializer,
        },
    ),
    update=extend_schema(
        summary="Update staff contact information",
        description="Update the contact information of a staff member.",
        tags=["Staff Related"],
        request=StaffContactInfoUpdateSerializer,
        responses={
            status.HTTP_200_OK: StaffContactInfoGetSerializer,
        },
    ),
    partial_update=extend_schema(
        summary="Partially update staff contact information",
        description="Partially update the contact information of a staff member.",
        tags=["Staff Related"],
        request=StaffContactInfoUpdateSerializer,
        responses={
            status.HTTP_200_OK: StaffContactInfoGetSerializer,
        },
    ),
)
class StaffContactInfoView(BaseStaffContactInfoView):
    permission_classes = [StaffContactInfoViewPolicy]
    def perform_update(self, serializer: Serializer):
        with transaction.atomic():
            instance = self.get_object()            

            AuditService.update_log(
                actor=self.request.user,
                instance=instance,
                validated_data=serializer.validated_data,
                request=self.request,
                description="Teacher Professional Info Update"
            )
            serializer.save()



"""_____________Admin Related Info___________________"""
from accounts.base_views import BaseAdminContactView
from accounts.permissions.policy import AdminContactInfoViewPolicy
from accounts.serializers import AdminContactInfoUpdateSerializer


@extend_schema_view(
    list=extend_schema(
        summary="List admin contact information",
        description="Retrieve contact information of administrators accessible to the authenticated user.",
        tags=["Admin Related"],
        responses={
            status.HTTP_200_OK: AdminContactInfoGetSerializer(many=True),
        },
    ),
    retrieve=extend_schema(
        summary="Retrieve admin contact information",
        description="Retrieve contact information for a specific administrator.",
        tags=["Admin Related"],
        responses={
            status.HTTP_200_OK: AdminContactInfoGetSerializer,
        },
    ),
    update=extend_schema(
        summary="Update admin contact information",
        description="Update the contact information of an administrator.",
        tags=["Admin Related"],
        request=AdminContactInfoUpdateSerializer,
        responses={
            status.HTTP_200_OK: AdminContactInfoUpdateSerializer,
        },
    ),
    partial_update=extend_schema(
        summary="Partially update admin contact information",
        description="Partially update the contact information of an administrator.",
        tags=["Admin Related"],
        request=AdminContactInfoUpdateSerializer,
        responses={
            status.HTTP_200_OK: AdminContactInfoUpdateSerializer,
        },
    ),
)
class AdminContactInfo(BaseAdminContactView):
    permission_classes = [AdminContactInfoViewPolicy]
    def perform_update(self, serializer: Serializer):
        with transaction.atomic():
            instance = self.get_object()            

            AuditService.update_log(
                actor=self.request.user,
                instance=instance,
                validated_data=serializer.validated_data,
                request=self.request,
                description="Teacher Professional Info Update"
            )
            serializer.save()


