from rest_framework.viewsets import ModelViewSet, GenericViewSet
from rest_framework.mixins import ListModelMixin, RetrieveModelMixin

# import serializer hare
from audit.serializers import AuditLogSerializer


# create base view

class BaseAuditView(ListModelMixin, RetrieveModelMixin, GenericViewSet):
    
    filterset_fields = {
        "action": ["iexact"],
        "actor": ["exact"],
        "content_type": ["exact"],
        "object_id": ["iexact"],
        "created_at": ["date", "gte", "lte"],
    }

    search_fields = [
        "description",
    ]

    ordering_fields = [
        "-created_at",
    ]
    
    serializer_class = AuditLogSerializer    
