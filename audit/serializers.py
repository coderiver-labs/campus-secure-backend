from rest_framework import serializers

# import models
from accounts.models import CustomUser
from audit.models import AuditLog




# test serializer
    
    


class AuditLogSerializer(serializers.ModelSerializer):
    actor = serializers.SerializerMethodField()
    class Meta:
        model = AuditLog
        fields = "__all__"
    def get_actor(self, obj):
        actor = {
            "uuid": str(obj.actor.uuid),
            "email": obj.actor.email,
            "role": obj.actor.role,
        }
        if obj.actor.role == "staff":
            actor.update({"position": obj.actor.staff_profile.position.name})
        return actor
            