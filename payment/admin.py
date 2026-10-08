from django.contrib import admin
from unfold.admin import ModelAdmin

# import models
from payment.models import FeePayment

# Register your models here.

@admin.register(FeePayment)
class AdminPayment(ModelAdmin):
    list_display = ("student", "student_class", "created_at", "month", "status")
    search_fields = ("student",)
    list_filter = ("student", "student_class")
    list_per_page = 50
    ordering = ["-created_at"]