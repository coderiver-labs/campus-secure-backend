
from rest_framework import serializers

# import models
from documents.models import UserDocument


# create serializers hare



class DocumentsSerializer(serializers.ModelSerializer):
    
    class Meta:
        model = UserDocument
        fields = "__all__"
        
        



# serializers.py
from rest_framework import serializers
from .models import UserDocument

class UserDocumentSerializer(serializers.ModelSerializer):
    file_url = serializers.SerializerMethodField()

    class Meta:
        model = UserDocument
        fields = ["uuid", "file_type", "file_url", "original_name", "file_format", "size", "created_at",]
        read_only_fields = ["uuid", "file_url", "original_name", "file_format", "size", "created_at"]

    def get_file_url(self, obj):
        request = self.context.get("request")
        if not obj.file or not request:
            return None
        # secure serve endpoint
        return f"http://127.0.0.1/documents/secure-file/{obj.uuid}/"

    def create(self, validated_data):
        request = self.context["request"]
        file = validated_data["file"]

        instance = UserDocument.objects.create(
            owner=request.user,
            file=file,
            file_type=validated_data.get("file_type"),
        )
        return instance


from rest_framework.exceptions import ValidationError
from documents.helper import VALIDATOR_MAP
from auth.validators import file_size_validator, validate_image

class UserProfileSerializer(serializers.ModelSerializer):
    class Meta:
        model = UserDocument
        fields = ["file"]

    def validate(self, attrs):
        file = attrs.get("file")
        attrs["file_type"] = "profile"
        try:
            validate_image(file=file)
        except ValidationError as e:
            raise serializers.ValidationError(e.detail)
        return attrs
        
    def create(self, validated_data):
        request = self.context.get("request")
        user = request.user
        file_type = validated_data["file_type"]
        file = validated_data["file"]
        
        instance, created = UserDocument.objects.update_or_create(owner=user,defaults={"file": file,"original_name": file.name, "file_type": file_type})
        print(instance)
        return instance
