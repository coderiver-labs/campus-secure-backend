from audit.utils import serialize_value
from audit.constants import EXCLUDED_FIELDS


# create diff hare


from audit.utils import serialize_value, sanitize_data

def get_model_diff(instance, updated_data: dict):
    before = {}
    after = {}

    for field, new_value in updated_data.items():
        old_value = getattr(instance, field, None)

        old_value = serialize_value(old_value)
        new_value = serialize_value(new_value)

        if old_value != new_value:
            before[field] = old_value
            after[field] = new_value

    # sanitize AFTER diff
    before = sanitize_data(before)
    after = sanitize_data(after)

    return before, after


from audit.utils import sanitize_data

def snapshot_instance(instance):
    data = {}

    for field in instance._meta.fields:
        field_name = field.name

        if field_name in EXCLUDED_FIELDS:
            continue

        value = getattr(instance, field_name)
        data[field_name] = serialize_value(value)

    return sanitize_data(data)