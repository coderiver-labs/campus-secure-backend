from django.urls import path, include

from rest_framework.routers import DefaultRouter

from school import views

router = DefaultRouter()

router.register("subject", views.SubjectViewSet, basename="subject_viewset")
router.register("class-level", views.ClassLevelViewSet, basename="class_level_viewset")
router.register("section", views.SectionViewSet, basename="section_viewset")
router.register("student-class", views.StudentClassViewSet, basename="student_class_viewset")
router.register("about", views.AboutViewSet, basename="about_viewset")
router.register("about-public", views.PublicAboutViewSet, basename="public_about_viewset")

urlpatterns = [
    path("", include(router.urls))
]
