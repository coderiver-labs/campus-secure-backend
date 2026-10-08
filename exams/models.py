from django.db import models
from django.utils import timezone
from django.core.validators import MinValueValidator

from accounts.models import BaseModel, StudentProfile, StudentClass, Subject



def today_date():
    return timezone.now().date()


def current_year():
    return timezone.now().year


class Exam(BaseModel):
    STATUS_CHOICES = [
        ("draft", "Draft"),
        ("ongoing", "Ongoing"),
        ("finished", "Finished"),
        ("published", "Published"),
    ]

    name = models.CharField(max_length=100)
    year = models.PositiveIntegerField(default=current_year)
    start_date = models.DateField(validators=[MinValueValidator(today_date)]) # shorbo nimno ajker date ar nise dile not allow
    end_date = models.DateField(validators=[MinValueValidator(today_date)])
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default="draft")
    is_active = models.BooleanField(default=True)
    description = models.TextField(max_length=2000, blank=True, null=True) # নতুন ফিল্ড
    
    class Meta:
        unique_together = ("name", "year")

    def __str__(self):
        return f"{self.name} - {self.year}"

    def clean(self):
        from django.core.exceptions import ValidationError
        super().clean()

        if self.start_date > self.end_date:
            raise ValidationError(
                {"end_date": "End date must be after start date."}
            )
        
    def save(self, *args, **kwargs):
        self.full_clean()
        super().save(*args, **kwargs)


class ExamClass(BaseModel):
    exam = models.ForeignKey(Exam, on_delete=models.CASCADE, related_name="exam_classes")
    student_class = models.ForeignKey(StudentClass, on_delete=models.CASCADE, related_name="exam_classes")

    class Meta:
        unique_together = ("exam", "student_class")

    def __str__(self):
        return f"{self.exam} - {self.student_class}"
    
    def clean(self):
        super().clean()
        from django.core.exceptions import ValidationError

        if self.exam.status in ["finished", "published"]:
            raise ValidationError({"exam": "Classes cannot be assigned to a finished or published exam."})
        
    def save(self, *args, **kwargs):
        self.full_clean()
        super().save(*args, **kwargs)



class ExamSubject(BaseModel):
    exam_start = models.DateTimeField()
    exam_end = models.DateTimeField()
    exam_class = models.ForeignKey(ExamClass, on_delete=models.CASCADE, related_name="exam_subjects")
    subject = models.ForeignKey(Subject, on_delete=models.CASCADE, related_name="exam_subjects")
    full_mark = models.DecimalField(max_digits=5, decimal_places=2)
    pass_mark = models.DecimalField(max_digits=5, decimal_places=2)

    class Meta:
        unique_together = ("exam_class", "subject")

        
    def clean(self):
        super().clean()

        from django.core.exceptions import ValidationError

        if self.pass_mark > self.full_mark:
            raise ValidationError("Pass mark cannot be greater than full mark.")

        if self.exam_start >= self.exam_end:
            raise ValidationError("Exam end time must be after start time.")

        exam = self.exam_class.exam

        if self.exam_start.date() < exam.start_date:
            raise ValidationError(
                "Exam subject cannot be scheduled before the exam start date."
            )

        if self.exam_end.date() > exam.end_date:
            raise ValidationError(
                "Exam subject cannot be scheduled after the exam end date."
            )

        allowed_subjects = self.exam_class.student_class.student_class_level.subjects.filter(uuid=self.subject.uuid).exists()
        if not allowed_subjects:
            raise ValidationError(f"'{self.subject}' is not offered for this class")
        

    def save(self, *args, **kwargs):
        self.full_clean()
        super().save(*args, **kwargs)


    def __str__(self):
        return f"{self.subject} - {self.exam_class}"



# Student Mark Models  
class StudentMark(BaseModel):
    exam_subject = models.ForeignKey(ExamSubject, on_delete=models.CASCADE, related_name="student_marks")
    student = models.ForeignKey(StudentProfile, on_delete=models.CASCADE, related_name="exam_marks")
    marks_obtained = models.DecimalField(max_digits=5, decimal_places=2)
    is_absent = models.BooleanField(default=False)

    class Meta:
        unique_together = ("exam_subject", "student")


    def clean(self):
        from django.core.exceptions import ValidationError

        exam_class = self.exam_subject.exam_class.student_class
        student_class = self.student.academic_info.student_class

        if exam_class != student_class:
            raise ValidationError("Student does not belong to this class.")

        if self.is_absent:
            if self.marks_obtained != 0:
                raise ValidationError("Absent student must have 0 marks.")

        if self.marks_obtained > self.exam_subject.full_mark:
            raise ValidationError("Marks cannot exceed full mark.")

    def save(self, *args, **kwargs):
        self.full_clean()
        super().save(*args, **kwargs)
        
        
    def __str__(self):
        return f"{self.student} - {self.exam_subject.subject} : {self.marks_obtained}"
