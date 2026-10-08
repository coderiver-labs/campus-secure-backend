from django.db import models
from django.contrib.auth.models import AbstractBaseUser, PermissionsMixin
from django.db.models import Q 

# import manager
from accounts.manager import UserManager

# import base Models
from accounts.base_model import BaseModel
from accounts.base_model import BaseHealthInfo, BaseParentsInfo, BaseProfileModel, BaseContactInfo
from accounts.base_model import BaseModel
from school.models import Subject, StudentClass


# import other
from django.utils import timezone




# Create your models here.



# custom user model
class CustomUser(AbstractBaseUser, PermissionsMixin, BaseModel):
    CHOICE = [
        ("admin", "Admin"),
        ("staff", "Staff"),
        ("teacher", "Teacher"),
        ("student", "Student"),
    ]
    
    first_name = models.CharField(max_length=100)
    last_name = models.CharField(max_length=100)
    email = models.EmailField(unique=True)
    role = models.CharField(max_length=10, choices=CHOICE, null=True, blank=True)
    
    is_active = models.BooleanField(default=True)
    is_staff = models.BooleanField(default=False)
    is_superuser = models.BooleanField(default=False)
    is_verified = models.BooleanField(default=False)
    
    objects = UserManager()
    USERNAME_FIELD = "email"
    REQUIRED_FIELDS = ["first_name", "last_name"]
    
    def save(self, *args, **kwargs):
        if not self._state.adding:   # means UPDATE
            old = CustomUser.objects.get(pk=self.pk)
            if old.role != self.role:
                raise ValueError("Role cannot be changed once set.")
        super().save(*args, **kwargs)

    def __str__(self):
        return f"{self.first_name} {self.last_name} ({self.email})"

    def get_full_name(self):
        return f"{self.first_name} {self.last_name}"
        

    class Meta:
        ordering = ["-created_at"]

        indexes = [
            models.Index(
                fields=["role"],
                name="user_role_idx",
            ),
        ]


class OneTimeToken(BaseModel):
    PURPOSE_CHOICES = [
        ("verify_email", "Email Verification"),
        ("reset_password", "Password Reset"),
        ("invite", "Invitation Link"),
    ]
    user = models.ForeignKey("CustomUser", on_delete=models.CASCADE)
    purpose = models.CharField(max_length=50, choices=PURPOSE_CHOICES)
    token = models.CharField(max_length=255)
    expired_at = models.DateTimeField()
    is_used = models.BooleanField(default=False)
    
    def is_valid(self):
        return not self.is_used and self.expired_at > timezone.now()
    
    class Meta:
        ordering = ["-created_at"]
    
    def __str__(self):
        return f"{self.user.email} - {self.purpose}"


# student profile model
class StudentProfile( BaseProfileModel):
    user = models.OneToOneField(CustomUser, on_delete=models.CASCADE, related_name="student_profile")

    def __str__(self):
        return f"{self.user.first_name} {self.user.last_name}"
    
    class Meta:
        ordering = ["-created_at"]

# Academic info
class StudentAcademicInfo(BaseModel):
    student = models.OneToOneField(StudentProfile, on_delete=models.CASCADE, related_name="academic_info")
    start_year = models.PositiveIntegerField(null=True, blank=True)
    end_year = models.PositiveIntegerField(null=True, blank=True)
    student_class = models.ForeignKey(StudentClass, on_delete=models.SET_NULL, null=True)
    roll_number = models.IntegerField(null=True, blank=True)
    admission_date = models.DateField(null=True, blank=True)
    previous_school = models.CharField(max_length=255, null=True, blank=True)
    
    def save(self, *args, **kwargs): # auto set start_year and end_year from admission_date
        if self.admission_date and not self.start_year:
            self.start_year = self.admission_date.year
            self.end_year = self.start_year + 1
        super().save(*args, **kwargs)
        
    class Meta:
        constraints = [
            models.UniqueConstraint(fields=["student_class", "roll_number"], name="unique_roll_per_class")
        ]
        ordering = ["-created_at"]

    def __str__(self):
        return f"{self.start_year}-{self.end_year} - {self.student.user.first_name}"
    
# student parents info
class StudentParentsInfo(BaseParentsInfo):
    student = models.OneToOneField(StudentProfile, on_delete=models.CASCADE, related_name="parents_info")
    def __str__(self):
        return f"Parents Info of {self.student.user.first_name} {self.student.user.last_name}"

# student info
class StudentContactInfo(BaseContactInfo):
    student = models.OneToOneField(StudentProfile, on_delete=models.CASCADE, related_name="contact_info")
    
    def __str__(self):
        return f"{self.student.user.first_name} {self.student.user.last_name}"
    
# student health info
class StudentHealthInfo(BaseHealthInfo):
    student = models.OneToOneField(StudentProfile, on_delete=models.CASCADE, related_name="health_info")

    def __str__(self):
        return f"Health Info of {self.student.user.first_name} {self.student.user.last_name}"







"""-------------> Teacher Profile <-------------"""

# teacher profile 
class TeacherProfile(BaseProfileModel):
    user = models.OneToOneField(CustomUser, on_delete=models.CASCADE, related_name="teacher_profile")

    def __str__(self):
        return f"{self.user.first_name} {self.user.last_name}"


# teacher Assignment
class TeacherAssignment(BaseModel):
    teacher = models.ForeignKey(TeacherProfile, on_delete=models.CASCADE, related_name="assignments")
    student_class = models.ForeignKey(StudentClass, on_delete=models.CASCADE, related_name="teacher_assignments")
    subject = models.ForeignKey(Subject, on_delete=models.CASCADE, related_name="teacher_assignments")

    class Meta:
        constraints = [
            models.UniqueConstraint(
                fields=["teacher", "student_class", "subject"],
                name="unique_teacher_assignment",
            )
        ]

    def clean(self):
        from django.core.exceptions import ValidationError
        super().clean()

        allowed = (self.student_class.student_class_level.subjects.filter(pk=self.subject.pk).exists())

        if not allowed:
            raise ValidationError(
                {
                    "subject": (
                        f"'{self.subject}' is not available for class "
                        f"{self.student_class.student_class_level.name}."
                    )
                }
            )
        
    def save(self, *args, **kwargs):
        self.full_clean()
        super().save(*args, **kwargs)


    def __str__(self):
        return (
            f"{self.teacher.user.get_full_name()} | "
            f"{self.student_class} | "
            f"{self.subject}"
        )


# ProfessionalInfo
class TeacherProfessionalInfo(BaseModel):
    teacher = models.OneToOneField(TeacherProfile, on_delete=models.CASCADE, related_name="professional_info")
    qualification = models.CharField(max_length=255, null=True, blank=True)
    years_of_experience = models.PositiveIntegerField(null=True, blank=True)
    subjects_specialization = models.CharField(max_length=255, null=True, blank=True)
    education_qualification = models.TextField(max_length=500, null=True, blank=True)
    
    def __str__(self):
        return f"Professional Info of {self.teacher.user.first_name} {self.teacher.user.last_name}"


# teacher contract info
class TeacherContactInfo(BaseContactInfo):
    teacher = models.OneToOneField(TeacherProfile, on_delete=models.CASCADE, related_name="contact_info")
    
    def __str__(self):
        return f"{self.teacher.user.first_name} {self.teacher.user.last_name}"


"""--------staff profile----------"""
# staff position
class StaffPosition(BaseModel):
    POSITION_CHOICES = [
        ("manager", "Manager"),
        ("principal", "Principal"),
        ("vice_principal", "Vice Principal"),
        ("head_clerk", "Head Clerk"),
        ("accounts", "Accounts Officer"),
        ("registrar", "Registrar"),
        ("it_officer", "IT Officer"),
        ("librarian", "Librarian"),

        # non-privileged
        ("cleaner", "Cleaner"),
        ("guard", "Guard"),
        ("driver", "Driver"),
        ("peon", "Peon"),
    ]

    name = models.CharField(max_length=20, choices=POSITION_CHOICES, unique=True)
    description = models.TextField(max_length=500, blank=True, null=True)
    
    def __str__(self):
        return self.name
 


# Staff Profile 
class StaffProfile(BaseProfileModel):
    user = models.OneToOneField(CustomUser, on_delete=models.CASCADE, related_name="staff_profile")
    position = models.ForeignKey(StaffPosition, on_delete=models.SET_NULL, null=True, blank=True, related_name="staff") # akhne kon jukti te ForeignKey use koresi
    def __str__(self):
        return f"{self.user.first_name} {self.user.last_name}"


# Staff Contact Info
class StaffContactInfo(BaseContactInfo):
    staff = models.OneToOneField(StaffProfile, on_delete=models.CASCADE, related_name="contact_info")
    
    def __str__(self):
        return f"{self.staff.user.first_name} {self.staff.user.last_name}"
    

"""--------admin profile----------"""

class AdminProfile(BaseProfileModel):
    user = models.OneToOneField(CustomUser, on_delete=models.CASCADE, related_name="admin_profile")

    def __str__(self):
        return f"{self.user.first_name} {self.user.last_name}"

# Admin Contact Info
class AdminContactInfo(BaseContactInfo):    
    admin = models.OneToOneField(AdminProfile, on_delete=models.CASCADE, related_name="contact_info")
    
    def __str__(self):
        return f"{self.admin.user.first_name} {self.admin.user.last_name}"
