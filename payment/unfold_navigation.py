from django.urls import reverse_lazy




# Create Navigation

PAYMENT_NAVIGATION = {
    "title": "Student Fee Payment",
    "icon": "school",
    "separator": True,
    "collapsible": True,
    "items": [
        {
            "title": "Payment",
            "icon": "payment",
            "link": reverse_lazy("admin:payment_feepayment_changelist")
        }
    ]
}