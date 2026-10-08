from django.shortcuts import get_object_or_404

# DRF
from rest_framework.exceptions import ValidationError as DRFValidationError # (যদি DRF ব্যবহার করেন)

# import models
from exams.models import ExamSubject

# others
import uuid


# create helpers 

def get_exam_subject(pk: uuid):
    try:
        if pk:
            uuid.UUID(str(pk)) 
    except ValueError:
        raise DRFValidationError({"exam_subject": "Not Valid UUID"})
    return get_object_or_404(ExamSubject, pk=pk)
