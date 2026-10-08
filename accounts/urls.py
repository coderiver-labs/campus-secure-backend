from django.urls import path, include
from accounts import views

# Define URL patterns for the accounts app


from rest_framework.routers import DefaultRouter
router = DefaultRouter()

# register viewsets here
router.register("manage-user", views.UserManagementAPI, basename="manage-user")

# router.register("test", views.TestViewSet, basename="test_api")
router.register("teacher-assignment", views.TeacherAssignmentAPI, basename="teacher-assignment")

# manage Student profile info 
router.register("student-academic-info", views.StudentAcademicInfoView, basename="student-academic-info")
router.register("student-parents-info", views.StudentParentsInfoView, basename="student-parents-info")
router.register("student-contact-info", views.StudentContactInfoView, basename="student-contact-info")
router.register("student-health-info", views.StudentHealthInfoView, basename="student-health-info")

# teacher profile related info
router.register("teacher-contact-info", views.TeacherContactInfoView, basename="teacher-contact-info"),
router.register("teacher-professional-info", views.TeacherProfessionalInfoView, basename="teacher-professional-info")

# Staff Profile Related Info
router.register("staff-position", views.StaffPositionView, basename="staff-position")
router.register("staff-contact-info", views.StaffContactInfoView, basename="staff-contact-info")

# admin Profile Related Info
router.register("admin-contact-info", views.AdminContactInfo, basename="admin-contact-info")


urlpatterns = [
    path('get-csrf-token/', views.GetCSRFToken.as_view(), name='get_csrf_token'),
    path("login/", views.LoginGenericAPIView.as_view(), name="login"),
    path("get-access-token/", views.GetAccessTOkenAPI.as_view(), name="get_access_token"),
    path("logout/", views.LogoutGenericAPIView.as_view(), name="logout"),
    
    # verify accounts 
    path('verify-account/<str:token>/', views.VerifyAccountAPI.as_view(), name='verify_account'),
    path('resend-verification-email/', views.ResendVerificationEmailAPI.as_view(), name='resend_verification_email'),

    # forget and reset password 
    path("forget-password/", views.ForgetPasswordAPI.as_view(), name="forget_password"),
    path("reset-password/<str:token>/", views.ResetPasswordAPI.as_view(), name="reset_password"),
    
    # change password
    path("change-password/", views.ChangePasswordAPI.as_view(), name="change_password"),
    
    # self profile
    path("profile/", views.ProfileAPIView.as_view(), name="self_profile"),

    path("api/", include(router.urls)),
]


