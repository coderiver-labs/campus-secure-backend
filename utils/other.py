from django.db.models import Model
from django.core.exceptions import ObjectDoesNotExist
def get_or_none(model:Model, **kwargs):
    try:
        return model.objects.get(**kwargs)
    except ObjectDoesNotExist:
        return None
