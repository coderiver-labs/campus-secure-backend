from django.db import models

# import models 
from accounts.base_model import BaseModel

# import validators
from auth.validators import validate_image

# Helpers
from school.helper import replace_file

# Create your models here.



# schools models
class Subject(BaseModel):
    
    name = models.CharField(max_length=100, unique=True)
    code = models.CharField(max_length=20, unique=True)
    description = models.TextField(blank=True, null=True)
    is_active = models.BooleanField(default=True)
    
    class Meta:
        ordering = ["name"]
    
    def __str__(self):
        return f"{self.name} - {self.code}"



# student class
class ClassLevel(BaseModel):
    CLASS_CHOICE = [
        ("1", "One"), ("2", "Two"),
        ("3", "Three"), ("4", "Four"),
        ("5", "Five"), ("6", "Six"),
        ("7", "Seven"), ("8", "Eight"),
        ("9", "Nine"), ("10", "Ten"),
    ]
    
    name = models.CharField(max_length=5, choices=CLASS_CHOICE, unique=True)
    monthly_fee = models.DecimalField(max_digits=6, decimal_places=2)
    subjects = models.ManyToManyField(Subject, related_name="class_levels")
    
    class Meta:
        unique_together = ("name",)
    
    def __str__(self):
        return self.get_name_display()
    
class Sections(BaseModel):
    SECTION_CHOICE = [
        ("A", "Section A"),
        ("B", "Section B"),
        ("C", "Section C"),
        ("D", "Section D"),
        ("E", "Section E"),
        ("F", "Section F"),
        ("G", "Section G"),
        ("H", "Section H"),
        ("I", "Section I"),
    ]
    section = models.CharField(choices=SECTION_CHOICE, max_length=1 , unique=True)
    
    def __str__(self):
        return self.get_section_display()
    
    
class StudentClass(BaseModel):
    student_class_level = models.ForeignKey(ClassLevel, on_delete=models.PROTECT, related_name="classes")
    section = models.ForeignKey(Sections, on_delete=models.PROTECT, related_name="classes")
    
    class Meta:
        unique_together = ("student_class_level", "section")
        
    def __str__(self):
        return f"{self.student_class_level} - {self.section}"



class About(BaseModel):
    """
    Stores the school's public/general information.

    This model is intended to have exactly one record.
    """

    title = models.CharField(max_length=255, default="About Our School",)
    short_description = models.TextField(blank=True,)
    description = models.TextField(blank=True,)
    mission = models.TextField(blank=True,)
    vision = models.TextField(blank=True,)
    established_year = models.PositiveIntegerField(null=True, blank=True,)
    address = models.TextField(blank=True,)
    contact_email = models.EmailField(blank=True,)
    contact_phone = models.CharField(max_length=30, blank=True,)
    website = models.URLField(blank=True,)
    logo = models.ImageField(upload_to="about/logo/", blank=True,)
    cover_image = models.ImageField(upload_to="about/cover/", blank=True,)
    metadata = models.JSONField(default=dict, blank=True,)

    class Meta:
        verbose_name = "About"
        verbose_name_plural = "About"

    def clean(self):
        if self.logo: validate_image(self.logo)
        if self.cover_image: validate_image(self.cover_image)
        


    def __str__(self):
        return self.title
    

    def save(self, *args, **kwargs):
        self.full_clean()

        if self.pk:
            old = type(self).objects.filter(pk=self.pk).first()

            if old:
                if self.logo != old.logo:
                    replace_file(old.logo, self.logo)

                if self.cover_image != old.cover_image:
                    replace_file(old.cover_image, self.cover_image)

        super().save(*args, **kwargs)




