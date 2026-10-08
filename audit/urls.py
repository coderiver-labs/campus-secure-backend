from django.urls import path, include

# DRF
from rest_framework.routers import DefaultRouter

# import views
from audit.views import AuditView

# create your router hare
router = DefaultRouter()
router.register("audit", AuditView, basename="audit_log")


# create url hare
urlpatterns = [
    path("", include(router.urls))
]
