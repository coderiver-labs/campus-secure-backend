from django.urls import path, include
from rest_framework.routers import DefaultRouter

# import views
from payment import views


# create urls hare



# create router
router = DefaultRouter()
router.register("fee-payment", views.FeePaymentManageView, basename="fee_payment")

# urls 
urlpatterns = [
    path("success/", views.SuccessPaymentAPIView.as_view(), name="success"),
    path("cancel/", views.CancelPaymentAPIView.as_view(), name="cancel"),
    path("stripe/webhook/", views.StripeWebhookView.as_view(), name="stripe_webhook"),

    path("school-fee-plan/", views.SchoolMonthlyPlanView.as_view(), name="school_fee_plan"),
    path("", include(router.urls)),
]
