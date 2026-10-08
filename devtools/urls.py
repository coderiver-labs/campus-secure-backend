from django.urls import path
from devtools import views

# Create path hare


urlpatterns = [
    path("get-error-500/", views.DivisionErrorView.as_view(), name="zero_division_error"),
    path("db-error/", views.DatabaseErrorView.as_view(), name="db_error"),
    path("2s-delay/", views.Delay2SecondsView.as_view(), name="2s_delay_view"),
    path("5s-delay/", views.Delay5SecondsView.as_view(), name="5s_delay_view"),
    path("10s-delay/", views.Delay10SecondsView.as_view(), name="10s_delay_view"),
    path("cpu-load/", views.CPUHeavyView.as_view(), name="cpu_heavy_load"),

    # celery error
    path("get-celery-error/", views.CeleryDivisionErrorView.as_view(), name="get_celery_error"),
    path("get-celery-success/", views.CelerySuccessView.as_view(), name="get_celery_success")
]