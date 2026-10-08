from django.urls import path, include
from exams import views

from rest_framework.routers import DefaultRouter

# router urls
router = DefaultRouter()

router.register("exam", views.ExamViewSet, basename="exam_viewset")
router.register("exam-class", views.ExamClassesViewSet, basename="exam_class")
router.register("exam-subject", views.ExamSubjectViewSet, basename="exam_subject_viewset")
router.register("student-mark", views.StudentMarkViewSet, basename="student_mark")

# Define URL patterns for the exams app
urlpatterns = [
    path("", include(router.urls)),
    path("exam-candidate/", views.ExamCandidateAPIViewSet.as_view()),
    path("exam-candidate/<str:pk>/", views.ExamCandidateAPIViewSet.as_view())
]