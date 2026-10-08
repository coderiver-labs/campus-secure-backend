from django.contrib import admin
from unfold.admin import ModelAdmin

# import models
from audit.models import AuditLog



# Register your models here.



@admin.register(AuditLog)
class AuditLodAdmin(ModelAdmin):
    list_display = ("actor", "action", "model_name")
    search_fields = ["actor"]
    ordering = ("-created_at",)