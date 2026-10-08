from django.contrib import admin
from unfold.admin import ModelAdmin

# import models
from exams.models import Exam, ExamClass, ExamSubject, StudentMark


# Register your models here.


@admin.register(Exam)
class ExamAdmin(ModelAdmin):
    list_display = ["name" ,"year" ,"status" ,"is_active"]
    search_fields = ["name", "year"]
    ordering = ["-created_at"]

@admin.register(ExamClass)
class ExamClassAdmin(ModelAdmin):
    list_display = ["exam" ,"student_class"]
    search_fields = ["exam"]
    ordering = ["-created_at"]


@admin.register(ExamSubject)
class ExamAdmin(ModelAdmin):
    list_display = ["exam_class" ,"subject" ,"full_mark" ,"pass_mark", "exam_start", "exam_end"]
    search_fields = ["exam_class", "subject"]
    ordering = ["-created_at"]



@admin.register(StudentMark)
class ExamAdmin(ModelAdmin):
    list_display = ["exam_subject" ,"student" ,"marks_obtained" ,"is_absent"]
    search_fields = ["student", "exam_subject"]
    ordering = ["-created_at"]