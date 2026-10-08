from rest_framework import serializers

# import models
from school.models import ClassLevel
from accounts.models import CustomUser
from payment.models import FeePayment


# create serializers hare







# public student Plan Serializer
class SchoolFeeSerializer(serializers.ModelSerializer):
    class Meta:
        model = ClassLevel
        fields = ["uuid", "name", "monthly_fee"]
        

from rest_framework import serializers
from payment.service.calculation import has_open_payment, remaining_month
class StudentFeeCheckoutSerializer(serializers.Serializer):
    email = serializers.EmailField(max_length=155)
    quantity = serializers.IntegerField(min_value=1, max_value=12)

    def validate(self, attrs):
        email = attrs["email"]
        quantity = attrs["quantity"]

        user = (
            CustomUser.objects
            .select_related(
                "student_profile",
                "student_profile__academic_info",
                "student_profile__academic_info__student_class",
                "student_profile__academic_info__student_class__student_class_level",
            ).filter(email=email,role="student",).first())

        if not user:
            raise serializers.ValidationError({"email": "Student not found."})

        student = user.student_profile

        # check failed or pending payment
        if has_open_payment(student=student):
            raise serializers.ValidationError({
                "payment": (
                    "An existing payment needs attention. "
                    "Please contact the school administration."
                )
            })

        remaining_months = remaining_month(student=student)
        

        attrs["user"] = user
        attrs["student"] = student
        attrs["remaining_months"] = remaining_months

        if remaining_months == 0:
            return attrs

        if quantity > remaining_months:
            raise serializers.ValidationError({"quantity": f"You can select maximum {remaining_months} months."})

        return attrs
    




"""__________________Payment Serializer_______________"""
class FeePaymentGetSerializer(serializers.ModelSerializer):
    student_class = serializers.SerializerMethodField()
    student = serializers.SerializerMethodField()

    class Meta:
        model = FeePayment
        fields = "__all__"

    def get_student_class(self, obj: FeePayment):
        return {"uuid": obj.student_class.uuid, "name": str(obj.student_class)} if obj.student_class else None

    def get_student(self, obj: FeePayment):
        student_info = {
            "uuid": f"{obj.student.user.uuid}",
            "name": f"{obj.student.user.first_name} {obj.student.user.last_name}",
            "class": f"{obj.student.academic_info.student_class.student_class_level.name}"
        }
        return student_info


from utils.serializers import READ_ONLY_FIELDS

class FeePaymentCUSerializer(serializers.ModelSerializer):
    class Meta:
        model = FeePayment
        exclude = READ_ONLY_FIELDS + ["paid_at", "stripe_session_id", "stripe_payment_intent",]
        



