from django.urls import reverse_lazy




# Create Navigation


AUDIT_NAVIGATION = {
    "title": "Audit Log",
    "separator": True,
    "collapsible": True,
    "items": [
        {
            "title": "Audit Log",
            "icon": "deployed_code_history",
            "link": reverse_lazy("admin:audit_auditlog_changelist")

        }
    ]
}