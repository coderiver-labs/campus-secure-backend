from rest_framework import serializers
from rest_framework.response import Response
from rest_framework import status
# import models
from exams.models import Exam, ExamClass, ExamSubject, StudentMark
from accounts.models import StudentClass

# read_only_fields 
from utils.serializers import READ_ONLY_FIELDS

# create serializer hare



class ExamSerializer(serializers.ModelSerializer):
    status = serializers.ChoiceField(choices=Exam.STATUS_CHOICES, required=False)

    class Meta:
        model = Exam
        fields = "__all__"
        read_only_fields = ("uuid", "year", "created_at", "updated_at")
        

    def validate(self, attrs: dict):
        """
        Handles cross-field validation for both create and update.
        """

        # Resolve values (supports partial updates)
        start_date = attrs.get("start_date", getattr(self.instance, "start_date", None))
        end_date = attrs.get("end_date", getattr(self.instance, "end_date", None))

        if start_date and end_date and start_date > end_date:
            raise serializers.ValidationError({"end_date": "End date must be after start date."})

        return attrs

    def _inject_year_from_start_date(self, validated_data: dict):
        start_date = validated_data.get("start_date")
        if start_date:
            validated_data["year"] = start_date.year
        return validated_data

    def create(self, validated_data: dict):
        validated_data.pop("status", None)
        validated_data = self._inject_year_from_start_date(validated_data)
        return super().create(validated_data)

    def update(self, instance, validated_data: dict):
        validated_data = self._inject_year_from_start_date(validated_data)
        return super().update(instance, validated_data)
    
    




""" ExamClass """ 
# GET
class ExamClassReadSerializer(serializers.ModelSerializer):
    exam = serializers.SerializerMethodField()
    student_class = serializers.SerializerMethodField()

    class Meta:
        model = ExamClass
        fields = "__all__"

    def get_exam(self, obj: ExamClass):
        return {
            "uuid": obj.exam.uuid, 
            "name": obj.exam.name, 
            "status": obj.exam.status, 
            "start": obj.exam.start_date, 
            "end": obj.exam.end_date
        } if obj.exam else None

    def get_student_class(self, obj: ExamClass):
        return {"uuid": obj.student_class.uuid, "name": str(obj.student_class)} if obj.student_class else None

# POST, PUT, PATCH
class ExamClassWriteSerializer(serializers.ModelSerializer):
    exam = serializers.SlugRelatedField(slug_field='uuid', queryset=Exam.objects.all())
    student_class = serializers.SlugRelatedField(slug_field='uuid', queryset=StudentClass.objects.all())

    class Meta:
        model = ExamClass
        fields = "__all__"
        read_only_fields = READ_ONLY_FIELDS
            





# GET
class ExamSubjectReadSerializer(serializers.ModelSerializer):
    exam_class = serializers.SerializerMethodField()
    subject = serializers.SerializerMethodField()

    class Meta:
        model = ExamSubject
        fields = ["uuid", "created_at", "updated_at", "exam_class", "subject", "full_mark", "pass_mark", "exam_start", "exam_end"]
        read_only_fields = READ_ONLY_FIELDS

    def get_exam_class(self, obj: ExamSubject):
        return {"uuid": obj.exam_class.uuid, "exam_class": str(obj.exam_class)} if obj.exam_class else None

    def get_subject(self, obj: ExamSubject):
        return {"uuid": obj.subject.uuid, "subject": str(obj.subject)} if obj.subject else None
    
    
# POST, PUT, PATCH
class ExamSubjectWriteSerializer(serializers.ModelSerializer):
    class Meta:
        model = ExamSubject
        fields = ["exam_class", "subject", "full_mark", "pass_mark", "exam_start", "exam_end"]
        read_only_fields = READ_ONLY_FIELDS
    

    
    def validate(self, attrs: dict):
        exam_class = attrs.get('exam_class')
        subject = attrs.get('subject')
        
        # Accessing the authorized subjects for this class level
        allowed_subjects = exam_class.student_class.student_class_level.subjects.all()

        if subject not in allowed_subjects:
            raise serializers.ValidationError({
                "subject": f"The subject '{subject.name}' is not assigned to {exam_class.student_class.student_class_level.name}."
            })

        if attrs.get('pass_mark') > attrs.get('full_mark'):
            raise serializers.ValidationError({
                "pass_mark": "Pass mark cannot be greater than the full mark."
            })

        return attrs


    def create(self, validated_data):
        instance = ExamSubject.objects.create(**validated_data)
        return instance

    def to_representation(self, instance):
        return ExamSubjectReadSerializer(instance).data
    
    




        
# list, retrieve
class StudentMarkReadSerializer(serializers.ModelSerializer):
    student = serializers.SerializerMethodField()
    exam_subject = serializers.SerializerMethodField()

    class Meta:
        model = StudentMark
        fields = "__all__"
        read_only_fields = READ_ONLY_FIELDS

    def get_student(self, obj: StudentMark):
        student_info = {
            "uuid": f"{obj.student.user.uuid}",
            "name": f"{obj.student.user.first_name} {obj.student.user.last_name}",
            "class": f"{obj.student.academic_info.student_class.student_class_level.name}"
        }
        return student_info


    def get_exam_subject(self, obj: StudentMark):
        return {"uuid": obj.exam_subject.subject.uuid, "subject": str(obj.exam_subject.subject.name)}


# Create, update
class StudentMarkSerializer(serializers.ModelSerializer):
    class Meta:
        model = StudentMark
        fields = "__all__"
        read_only_fields = READ_ONLY_FIELDS

    def to_representation(self, instance):
        return StudentMarkReadSerializer(instance).data
    


from accounts.models import StudentAcademicInfo, StudentProfile
from school.models import StudentClass
from django.shortcuts import get_list_or_404
class ExamCandidateSerializer(serializers.ModelSerializer):
    student = serializers.SerializerMethodField()
    student_class = serializers.SerializerMethodField()
    class Meta:
        model = StudentAcademicInfo
        exclude = ["created_at", "updated_at", "previous_school", "admission_date"]

    def get_student(self, obj: StudentAcademicInfo):
        full_name = obj.student.user.get_full_name()
        uuid = obj.student.uuid
        return {"uuid": uuid, "full_name": full_name}
    
    def get_student_class(self, obj: StudentAcademicInfo):
        uuid = obj.student_class_id
        class_level = obj.student_class.student_class_level.name
        return {"uuid": uuid, "class_level": class_level}
    
    

