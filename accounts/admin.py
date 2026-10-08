from django.contrib import admin
from unfold.admin import ModelAdmin

# import models
from accounts.models import (
    CustomUser, 
    StudentProfile, StudentContactInfo, StudentParentsInfo, StudentHealthInfo, StudentAcademicInfo,
    TeacherProfile, TeacherContactInfo, TeacherProfessionalInfo,
    StaffProfile, StaffPosition, StaffContactInfo,
    AdminProfile, AdminContactInfo
)

def get_user_full_name(obj):
    return f"{obj.user.first_name} {obj.user.last_name}" if obj.user else "-"

def get_user_email(obj):
    return obj.user.email if obj.user else "-"


# Custom User Admin
@admin.register(CustomUser)
class CustomUserAdmin(ModelAdmin):
    list_display = ("first_name", "last_name", "email", "role", "is_active", "is_verified")
    search_fields = ("first_name", "last_name", "email")
    list_filter = ("role", "is_active", "is_staff", "is_verified", "created_at")
    list_per_page = 50


# Student Related Admins
@admin.register(StudentProfile)
class StudentProfileAdmin(ModelAdmin):
    list_display = (get_user_full_name, get_user_email, "gender", "date_of_birth")
    search_fields = ("user__first_name", "user__last_name", "user__email")
    list_filter = ("gender", "created_at")
    ordering = ["-created_at"]
    
@admin.register(StudentAcademicInfo)
class StudentAcademicInfoAdmin(ModelAdmin):
    list_display = ("student", "student_class", "roll_number", "start_year", "end_year")
    search_fields = ("student__user__first_name", "student__user__email", "roll_number")
    list_filter = ("student_class", "start_year")
    ordering = ["-created_at"]
    
@admin.register(StudentHealthInfo)
class StudentHealthInfoAdmin(ModelAdmin):
    list_display = ("student", "blood_group", "allergies")
    search_fields = ("student__user__first_name", "student__user__email")
    list_filter = ("blood_group",)
    
@admin.register(StudentContactInfo)
class StudentContactInfoAdmin(ModelAdmin):
    list_display = ("student", "phone", "address")
    search_fields = ("student__user__first_name", "phone", "address")

@admin.register(StudentParentsInfo)
class StudentParentsInfoAdmin(ModelAdmin):
    list_display = ("student", "father_name", "mother_name", "father_phone")
    search_fields = ("student__user__first_name", "father_name", "mother_name")


# Teacher Related Admins
@admin.register(TeacherProfile)
class TeacherProfileAdmin(ModelAdmin):
    list_display = (get_user_full_name, get_user_email)
    search_fields = ("user__first_name", "user__last_name", "user__email")
    ordering = ["-created_at"]

from accounts.models import TeacherAssignment
@admin.register(TeacherAssignment)
class TeacherAssignment(ModelAdmin):
    list_display = ("teacher", "student_class", "subject")
    search_fields = ("teacher__user__first_name", "teacher__user__first_name", "teacher__user__email")
    ordering = ["-created_at"]


@admin.register(TeacherProfessionalInfo)
class TeacherProfessionalInfoAdmin(ModelAdmin):
    list_display = ("teacher", "qualification", "years_of_experience")
    search_fields = ("teacher__user__first_name", "qualification")
    list_filter = ("years_of_experience",)

@admin.register(TeacherContactInfo)
class TeacherContactInfoAdmin(ModelAdmin):
    list_display = ("teacher", "phone", "emergency_contact")
    search_fields = ("teacher__user__first_name", "phone")


# Staff Related Admins
@admin.register(StaffPosition)
class StaffPositionAdmin(ModelAdmin):
    list_display = ("name", "description")
    search_fields = ("name",)

@admin.register(StaffProfile)
class StaffProfileAdmin(ModelAdmin):
    list_display = (get_user_full_name, "position")
    list_filter = ("position",)
    search_fields = ("user__first_name", "position__name")
    ordering = ["-created_at"]

@admin.register(StaffContactInfo)
class StaffContactInfoAdmin(ModelAdmin):
    list_display = ("staff", "phone")
    search_fields = ("staff__user__first_name", "phone")

# Admin Related Admins
@admin.register(AdminProfile)
class AdminProfileAdmin(ModelAdmin):
    list_display = (get_user_full_name, get_user_email)
    search_fields = ("user__first_name", "user__email")

@admin.register(AdminContactInfo)
class AdminContactInfoAdmin(ModelAdmin):
    list_display = ("admin", "phone")
    search_fields = ("admin__user__first_name", "phone")


from accounts.models import OneTimeToken

@admin.register(OneTimeToken)
class OneTimeTokenAdmin(ModelAdmin):
    list_display = ["user", "purpose", "expired_at", "is_used"]
    search_fields = ["user__first_name", "purpose"]
    ordering = ["-created_at"]





# accounts/admin.py এর একদম নিচে এটি পেস্ট করুন

# from django.contrib import admin
# from accounts.dashboard import admin_dashboard_callback

# # Django Admin এর মূল সাইট ক্লাসকে হুক করা
# admin.site.index = lambda request, extra_context=None: admin.site.__class__.index(
#     admin.site,
#     request,
#     extra_context=admin_dashboard_callback(request, extra_context or {})
# )