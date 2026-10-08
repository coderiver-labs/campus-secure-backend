

# import models
from payment.models import FeePayment

# import serializer
from payment.serializers import FeePaymentGetSerializer, FeePaymentCUSerializer


# import utils
from utils.base_view import BasePaymentRelatedView


# create base views

from payment.filtering import StudentAcademicInfoFilter
class BaseFeePaymentView(BasePaymentRelatedView):

    def get_serializer_class(self):
        if self.action in ["create", "update", "partial_update"]:
            return FeePaymentCUSerializer
        return FeePaymentGetSerializer

    queryset = FeePayment.objects.select_related(
        "student",
        "student_class"
    )
    
    filterset_class = StudentAcademicInfoFilter

    search_fields = [
        "student__user__first_name",
        "student__user__last_name",
        "student__user__email",
    ]

    ordering = ["-created_at"]



    



