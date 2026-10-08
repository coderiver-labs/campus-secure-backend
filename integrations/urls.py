from django.urls import path, include

from integrations import views

urlpatterns = [
    path("webhook/", views.SentryWebhookView.as_view(), name="sentry_webhook_view")
]