from django.db.models.fields.files import FieldFile


# serializer helper
def serialize_value(value):
    if isinstance(value, FieldFile):
        return value.name

    if isinstance(value, dict):
        return {
            key: serialize_value(val)
            for key, val in value.items()
        }

    if isinstance(value, (list, tuple)):
        return [serialize_value(item) for item in value]

    return value




# models helper
def replace_file(old_file, new_file):
    if old_file and old_file.name:
        old_file.delete(save=False)
    return new_file