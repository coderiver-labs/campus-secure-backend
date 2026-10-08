from django.contrib.contenttypes.models import ContentType
from django.db.models import Model
from django.db import transaction


# DRF
from rest_framework.request import HttpRequest

# import models
from accounts.models import CustomUser

from audit.models import AuditLog
from audit.diff import get_model_diff, snapshot_instance

# import audit utils
from audit.utils import get_client_ip

# import celery
from celery_task.task import async_log_audit 

# create AuditLogs service hare

class AuditService:
    
    @staticmethod
    def _get_common_info(request: HttpRequest):
        return {
            "ip_address": get_client_ip(request),
            "user_agent": request.META.get("HTTP_USER_AGENT", "") if request else None
        }


    @classmethod
    def log(cls, actor: CustomUser | None, instance: Model, action: str, before: dict=None, after: dict=None, request: HttpRequest=None, description: str=""):
        """Centralized logging method with Celery and Transaction safety"""
        common_info = cls._get_common_info(request)
        ctype = ContentType.objects.get_for_model(instance)
        
        actor_uuid = actor.uuid if actor else None
        ctype_id = ctype.id
        object_uuid = str(getattr(instance, 'uuid', ''))
        model_name = instance.__class__.__name__

        transaction.on_commit(lambda: async_log_audit.delay(
            actor_uuid=actor_uuid,
            ctype_id=ctype_id,
            object_uuid=object_uuid,
            model_name=model_name,
            action=action,
            before=before,
            after=after,
            common_info=common_info,
            description=description
        ))


    @classmethod
    def create_log(cls, actor: CustomUser | None, instance: Model, request: HttpRequest=None, description: str=""):
        after = snapshot_instance(instance)
        return cls.log(actor, instance, "CREATE", after=after, request=request, description=description)

    @classmethod
    def update_log(cls, actor: CustomUser | None, instance: Model, validated_data: dict, request: HttpRequest=None, description: str=""):
        if isinstance(instance, tuple):
            instance = instance[0]
        before, after = get_model_diff(instance, validated_data)
        if not before and not after: # jodi kono change na hoy tahole kono audit add korbena
            return None
        return cls.log(actor, instance, "UPDATE", before=before, after=after, request=request, description=description)

    @classmethod
    def delete_log(cls, actor: CustomUser | None, instance: Model, request: HttpRequest=None, description: str=""):
        before = snapshot_instance(instance)
        return cls.log(actor, instance, "DELETE", before=before, request=request, description=description)
