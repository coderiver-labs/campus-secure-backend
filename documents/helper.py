# import python
import uuid

# import validator
from auth.validators import validate_pdf, validate_image

# create helper hare 


# validate image or other file
VALIDATOR_MAP = {
    "profile": validate_image,
    "father_image": validate_image,
    "mother_image": validate_image,
    "father_nid": validate_pdf,
    "mother_nid": validate_pdf,

    "teacher_profile": validate_image,
    "admin_profile": validate_image,
    
}

# file rename or dir path creator
def document_upload_path(instance, filename:str):
    """Dynamic upload path: protected_file/<file_type>/<user_id>/<uuid>.<ext>"""
    folder_map = {
        "profile": "profile",
        "father_image": "father_image",
        "mother_image": "mother_image",
        "father_nid": "father_nid",
        "mother_nid": "mother_nid",
        "teacher_profile": "teacher_profile",
        "admin_profile": "admin_profile",
        "marksheet": "marksheets",
        "other": "other",
    }

    folder = folder_map.get(instance.file_type, "other")
    ext = filename.split(".")[-1]
    unique_name = f"{uuid.uuid4().hex}.{ext}"
    return f"protected_file/{folder}/{instance.owner.uuid}/{unique_name}"

# model choice 
FILE_TYPE_CHOICE = [
        ("profile", "Profile"),
        ("father_image", "Father Image"),
        ("mother_image", "Mother Image"),
        ("father_nid", "Father NID"),
        ("mother_nid", "Mother NID"),
        ("teacher_profile", "Teacher Profile"),
        ("admin_profile", "Admin Profile"),
        ("other", "Other")
    ]
