from django.db import models

# import models
from accounts.models import BaseModel, CustomUser

# import tools
import magic

# import validator
from auth.validators import file_size_validator

# import helpers
from documents.helper import document_upload_path, VALIDATOR_MAP, FILE_TYPE_CHOICE

# import utils
from utils.storages import ProtectedFileSystemStorage

# Create your models here.



class UserDocument(BaseModel):
    owner = models.ForeignKey(CustomUser, on_delete=models.CASCADE)
    file_type = models.CharField(max_length=50, choices=FILE_TYPE_CHOICE)
    file = models.FileField(upload_to=document_upload_path, storage=ProtectedFileSystemStorage())
    original_name = models.CharField(max_length=255, null=True, blank=True)
    file_format = models.CharField(max_length=100, null=True, blank=True)  # ← ঠিক করো এখানে
    size = models.BigIntegerField(null=True, blank=True)

    allowed_roles = models.JSONField(blank=True, null=True)
    allowed_users = models.ManyToManyField(CustomUser, related_name="shared_files", blank=True)



    def __str__(self):
        return f"{self.original_name} ({self.owner})"

    def clean(self):
        file = self.file
        if not file: return

        validator = VALIDATOR_MAP.get(self.file_type, file_size_validator, )
        validator(file=file)


    def save(self, *args, **kwargs):
        old_file = None

        # Existing object file reference 
        if self.pk:
            try:
                old_instance = type(self).objects.get(pk=self.pk)
                old_file = old_instance.file
            except type(self).DoesNotExist:
                pass

        # Validation
        self.full_clean()

        # New file tahkle metadata create
        if self.file:
            file_mime = magic.from_buffer(
                self.file.read(2048),
                mime=True,
            )

            self.file.seek(0)

            self.file_format = file_mime
            self.size = self.file.size
            self.original_name = self.file.name
            
        super().save(*args, **kwargs)

        # delete old file
        if old_file and old_file.name and old_file.name != self.file.name:
            old_file.delete(save=False)

    def has_access(self, user):
        if user == self.owner:
            return True
        if self.allowed_users.filter(id=user.id).exists():
            return True
        if self.allowed_roles and user.role in self.allowed_roles:
            return True
        return False

    class Meta:
        ordering = ["-created_at"]

        constraints = [
            models.UniqueConstraint(
                fields=["owner", "file_type"],
                name="unique_owner_file_type",
            )
        ]