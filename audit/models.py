from django.db import models

# Create your models here.



from django.db import models
from django.contrib.contenttypes.models import ContentType
from django.contrib.contenttypes.fields import GenericForeignKey

from accounts.base_model import BaseModel


# import django-prometheus




class AuditLog(BaseModel):
    ACTION_CHOICES = (
        ("CREATE", "Create"),
        ("UPDATE", "Update"),
        ("DELETE", "Delete"),
    )
    
    actor = models.ForeignKey("accounts.CustomUser", null=True, on_delete=models.SET_NULL, related_name="audit_logs")

    # db_index=True দিলে কুয়েরি ফাস্ট হয়
    action = models.CharField(max_length=20, choices=ACTION_CHOICES, db_index=True)
    
    # Generic relation
    content_type = models.ForeignKey(ContentType, on_delete=models.CASCADE) # ataw model ar info dei kinto number a 
    object_id = models.UUIDField(db_index=True) 
    content_object = GenericForeignKey("content_type", "object_id")
    
    # Change tracking
    before = models.JSONField(null=True, blank=True)
    after = models.JSONField(null=True, blank=True)

    # Metadata
    ip_address = models.GenericIPAddressField(null=True, blank=True)
    user_agent = models.TextField(null=True, blank=True)
    
    # model ar name ke show korar jonno ata add kora hoyese 
    model_name = models.CharField(max_length=100, null=True, blank=True, db_index=True)
    description = models.TextField(blank=True)

    class Meta:
        indexes = [
            models.Index(fields=["content_type", "object_id"]),
            models.Index(fields=["model_name", "action"]), # কম্বাইন্ড ইন্ডেক্স
            models.Index(fields=["actor"]),
            models.Index(fields=["action"]),
            models.Index(fields=["created_at"]),
        ]
        ordering = ["-created_at"]
    
    def __str__(self):
        return f"{self.actor} - {self.action} - {self.object_id}"