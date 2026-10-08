from django.contrib import admin
from unfold.admin import ModelAdmin

# import models 
from school.models import Subject, ClassLevel, Sections, StudentClass, About


# Register your models here.


@admin.register(Subject)
class SubjectAdmin(ModelAdmin):
    list_display = ["name", "code", "is_active"]
    search_fields = ["name", "code"]
    ordering = ["-created_at"]

@admin.register(StudentClass)
class StudentClassAdmin(ModelAdmin):
    list_display = ("student_class_level", "section")
    search_fields = ("student_class_level__name", "section__section")
    ordering = ("student_class_level__name", "section__section")
    

@admin.register(ClassLevel)
class ClassLevelAdmin(ModelAdmin):
    list_display = ("name", "monthly_fee")
    search_fields = ("name", "monthly_fee")
    ordering = ("name", "monthly_fee")

@admin.register(Sections)
class SectionsAdmin(ModelAdmin):
    list_display = ("section",)
    search_fields = ("section",)
    ordering = ("section",)

@admin.register(About)
class AboutAdmin(ModelAdmin):
    list_display = ("title", "address", "contact_email", "contact_phone")
    search_fields = ("address", "contact_email", "contact_phone")
