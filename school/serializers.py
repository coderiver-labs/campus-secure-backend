
from rest_framework import serializers

# import models
from school.models import Subject, ClassLevel, Sections, StudentClass

# import utils
from utils.serializers import READ_ONLY_FIELDS

# create your serializers


class SubjectSerializer(serializers.ModelSerializer):
    
    class Meta:
        model = Subject
        fields = "__all__"
        read_only_fields = READ_ONLY_FIELDS
        


# minimal serializer for service serializer 
class SubjectMinimalSerializer(serializers.ModelSerializer):
    class Meta:
        model = Subject
        fields = ['uuid', 'name', "code"]
        



class ClassLevelSerializer(serializers.ModelSerializer):

    subjects = serializers.PrimaryKeyRelatedField(queryset=Subject.objects.all(),  many=True)

    class Meta:
        model = ClassLevel
        fields = ["uuid", "created_at", "updated_at", "name", "monthly_fee", "subjects"]
        read_only_fields = READ_ONLY_FIELDS

    def to_representation(self, instance: ClassLevel):
        representation = super().to_representation(instance)
        representation['subjects'] = SubjectMinimalSerializer(instance.subjects.all(), many=True).data
        return representation


class SectionSerializer(serializers.ModelSerializer):
    class Meta:
        model = Sections
        fields = "__all__"
        read_only_fields = READ_ONLY_FIELDS
        



# minimal section and class-level
class ClassLevelMinimalSerializer(serializers.ModelSerializer):
    class Meta:
        model = ClassLevel
        fields = ["uuid", "name"]
    
class SectionSerializer(serializers.ModelSerializer):
    class Meta:
        model = Sections
        fields = ["uuid", "section"]



class StudentClassListSerializer(serializers.ModelSerializer):
    student_class_level = ClassLevelMinimalSerializer(read_only= True)
    section = SectionSerializer(read_only=True)

    class Meta:
        model = StudentClass
        fields = ["uuid", "created_at", "updated_at", "student_class_level", "section"]
        read_only_fields = READ_ONLY_FIELDS



class StudentClassSerializer(serializers.ModelSerializer):
    class Meta:
        model = StudentClass
        fields = "__all__"
        read_only_fields = READ_ONLY_FIELDS



"""_________About Serializer_________"""
# About Serializer
from school.models import About
class AboutAdminSerializer(serializers.ModelSerializer):
    class Meta:
        model = About
        fields = "__all__"
        read_only_fields = READ_ONLY_FIELDS


class AboutPublicSerializer(serializers.ModelSerializer):
    class Meta:
        model = About
        exclude = READ_ONLY_FIELDS

        
