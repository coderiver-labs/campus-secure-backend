from django.db import models


# import python package or other 
import uuid


# create base model hare


class BaseModel(models.Model):
    uuid = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        abstract = True
        
        
class BaseProfileModel(BaseModel):
    GENDER_CHOICES = [
        ("F", "Female"),
        ("M", "Male"),
        ("O", "Other")
    ]
    gender = models.CharField(max_length=1, choices=GENDER_CHOICES)
    date_of_birth = models.DateField(null=True, blank=True)

    class Meta:
        abstract = True

# contract info
class BaseContactInfo(BaseModel):
    phone = models.CharField(max_length=25, null=True, blank=True)
    address = models.CharField(max_length=1000, null=True, blank=True)
    emergency_contact = models.CharField(max_length=25, null=True, blank=True)

    class Meta:
        abstract = True

class BaseParentsInfo(BaseModel):
    father_name = models.CharField(max_length=200, null=True, blank=True)
    father_phone = models.CharField(max_length=25, null=True, blank=True)
    father_email = models.EmailField(max_length=155, null=True, blank=True)
    mother_name = models.CharField(max_length=200, null=True, blank=True)
    mother_phone = models.CharField(max_length=25, null=True, blank=True)
    mother_email = models.EmailField(max_length=155, null=True, blank=True)

    class Meta:
        abstract = True

    

class BaseHealthInfo(BaseModel):
    BLOOD_CHOICE = [
        ('A+', 'A+'), ('A-', 'A-'),
        ('B+', 'B+'), ('B-', 'B-'),
        ('O+', 'O+'), ('O-', 'O-'),
        ('AB+', 'AB+'), ('AB-', 'AB-')
    ]
    
    blood_group = models.CharField(max_length=5, choices=BLOOD_CHOICE, null=True, blank=True)
    height_cm = models.DecimalField(max_digits=5, decimal_places=2, null=True, blank=True)
    weight_kg = models.DecimalField(max_digits=5, decimal_places=2, null=True, blank=True)

    allergies = models.JSONField(default=list, blank=True)
    medical_conditions = models.JSONField(default=list, blank=True)
    medications = models.JSONField(default=list, blank=True)
    
    emergency_contact_name = models.CharField(max_length=100, null=True, blank=True)
    emergency_contact_phone = models.CharField(max_length=25, null=True, blank=True)
    emergency_contact_relation = models.CharField(max_length=50, null=True, blank=True)


    class Meta:
        abstract = True

class OtherInfo(BaseModel):
    guardian = models.CharField(max_length=100, null=True, blank=True)
    guardian_contact = models.CharField(max_length=25, null=True, blank=True)
    remarks = models.CharField(max_length=255, null=True, blank=True)
    status = models.BooleanField(default=True)

    class Meta:
        abstract = True
        
        

# employee base model
class BaseEmployeeModel(BaseProfileModel, BaseContactInfo, OtherInfo):
    employee_id = models.CharField(max_length=50, unique=True)

    class Meta:
        abstract = True