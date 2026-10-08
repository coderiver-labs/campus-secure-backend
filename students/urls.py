from django.urls import path, include

from rest_framework.routers import DefaultRouter

# import views
from students import views


router = DefaultRouter()

router.register("student-profile", views.StudentProfileViewSet, basename="student_profile_viewset")


urlpatterns = [
    path("", include(router.urls))
]