from django.contrib import admin

# import models hare
from documents.models import UserDocument


# Register your models here.


@admin.register(UserDocument)
class UserDocumentAdmin(admin.ModelAdmin):
    list_display = ("owner", "file_type", "original_name", "created_at", "updated_at")
    readonly_fields = ("uuid", "created_at", "updated_at")  # যাতে user edit করতে না পারে
    search_fields = ("owner__username", "original_name")
    list_filter = ("file_type", "created_at")


