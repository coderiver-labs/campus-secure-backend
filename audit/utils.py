from rest_framework.request import HttpRequest

# import constants
from audit.constants import SENSITIVE_FIELDS

# import py
import uuid
from datetime import datetime, date
from decimal import Decimal


# create utils hare



def get_client_ip(request: HttpRequest):
    if not request: return None
    x_forwarded_for: str = request.META.get("HTTP_X_FORWARDED_FOR")
    return x_forwarded_for.split(",")[0].strip() if x_forwarded_for else request.META.get("REMOTE_ADDR")



from django.db.models import Manager
from django.db.models.query import QuerySet

def serialize_value(value):
    if value is None:
        return None
    
    # jodi ata serializer validate_data theke kono list ashse jemon subject list
    if isinstance(value, list):
        return [serialize_value(item) for item in value]

    # ManyToMany  
    if isinstance(value, (Manager, QuerySet)):
        return [str(obj.uuid) for obj in value.all()]

    if isinstance(value, uuid.UUID):
        return str(value)
    
    if isinstance(value, (datetime, date)):
        return value.isoformat()
    
    if isinstance(value, Decimal):
        return float(value)
    
    if hasattr(value, "uuid"):
        return str(value.uuid)
        
    return value

# for sensitive data filtering
def sanitize_data(data: dict):
    cleaned = {}

    for key, value in data.items():
        if key in SENSITIVE_FIELDS:
            cleaned[key] = "***REDACTED***"
        else:
            cleaned[key] = value

    return cleaned

