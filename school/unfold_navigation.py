from django.urls import reverse_lazy




# Create Navigation

SCHOOL_NAVIGATION = {
    "title": "School Academic Setup",
    "icon": "school",
    "separator": True,
    "collapsible": True,
    "items": [
        {
            "title": "Subject",
            "icon": "menu_book",
            "link": reverse_lazy("admin:school_subject_changelist")
        },
        {
            "title": "Class Level",
            "icon": "stairs",
            "link": reverse_lazy("admin:school_classlevel_changelist")
        },
        {
            "title": "Section",
            "icon": "view_module",
            "link": reverse_lazy("admin:school_sections_changelist")
        },
        {
            "title": "Student Class",
            "icon": "groups",
            "link": reverse_lazy("admin:school_studentclass_changelist")
        },
        {
            "title": "About",
            "icon": "info",
            "link": reverse_lazy("admin:school_about_changelist")
        }
    ]
}