from utils.base_view import BaseCRUModelViewSet

# import models
from accounts.models import StudentProfile

# import serializer
from students.serializers import StudentProfileSerializer

# import filtering
from students.filtering import StudentAcademicInfoFilter



# Create Base_views

class BaseStudentProfileViewSet(BaseCRUModelViewSet):
    serializer_class = StudentProfileSerializer
    queryset = StudentProfile.objects.select_related("user")
    filterset_class = StudentAcademicInfoFilter

    search_fields = [
        "user__first_name",
        "user__last_name",
    ]

    ordering_fields = ["created_at", "updated_at"]

    ordering = ["-created_at"]

