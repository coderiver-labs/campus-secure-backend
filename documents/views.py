from django.http import HttpResponse, Http404
from django.shortcuts import get_object_or_404

# DRF
from rest_framework.generics import GenericAPIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework.parsers import MultiPartParser, FormParser

# import models
from documents.models import UserDocument

# import serializers
from documents.serializers import UserProfileSerializer

# docs
from drf_spectacular.utils import extend_schema, extend_schema_view, OpenApiResponse



# Create your views here.

@extend_schema_view(
    get=extend_schema(
        tags=["Profile"],
        summary="Retrieve Profile Picture",
        description=(
            "Securely retrieve the authenticated user's profile picture. "
            "The protected file is served through NGINX using X-Accel-Redirect. "
            "Only authenticated users with the required permission can access "
            "the profile picture."
        ),
    ),
    post=extend_schema(
        tags=["Profile"],
        summary="Set Profile Picture",
        description=(
            "Upload and set a profile picture for the authenticated user. "
            "The uploaded file is validated and stored as the user's "
            "protected profile document."
        ),
        request=UserProfileSerializer,
        responses={
            200: OpenApiResponse(
                description="Profile picture set successfully."
            ),
        },
    ),
)
class UserProfilePictureAPI(GenericAPIView):
    """
    Securely serve protected files through NGINX (X-Accel-Redirect).
    Only authenticated users with permission can access.
    """
    parser_classes = [MultiPartParser, FormParser]
    serializer_class = UserProfileSerializer
    
    def get_object(self):
        try:
            obj = get_object_or_404(UserDocument, owner=self.request.user, file_type="profile")
            return obj
        except Exception as e:
            raise Http404("Profile picture Not Set ")
    
    def get(self, request):
        document:UserDocument = self.get_object()
        internal_path = document.file.name
        response = HttpResponse()
        response["Content-Type"] = document.file_format or "application/octet-stream"
        response["Content-Disposition"] = f'inline; filename="{document.original_name}"'
        response["X-Accel-Redirect"] = f"/internal_protected/{internal_path}"
        return response

    def post(self, request):
        serializer = self.get_serializer(data=request.data, context={"request": request})
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response({"message": "profile set successfully"}, status=status.HTTP_200_OK)

