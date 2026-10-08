

# from django.forms import ValidationError
from rest_framework.exceptions import AuthenticationFailed, ValidationError

# create helpers here.


def file_size_validator(file):
    """Validate if the uploaded file is within 2MB."""
    if file.size > 2 * 1024 * 1024:
        raise ValidationError({"file": f"File {file.name} size must be under 2MB."})
    return True
