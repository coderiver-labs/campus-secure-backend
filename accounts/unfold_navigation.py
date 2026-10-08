from django.urls import reverse_lazy


# Create Unfold Admin Panel


UNFOLD_USERS_NAVIGATION = {
    "title": "Accounts / Users",
    "separator": True,
    "collapsible": True,
    "items": [
        {
            "title": "Custom Users",
            "icon": "people",
            "link": reverse_lazy("admin:accounts_customuser_changelist")
        }
    ]
}


UNFOLD_STUDENT_PROFILE_NAVIGATION = {
    "title": "Student Management",
    "separator": True,
    "collapsible": True,
    "items": [
        {
            "title": "Student Profiles",
            "icon": "school",
            "link": reverse_lazy("admin:accounts_studentprofile_changelist"),
        },
        {
            "title": "Academic Infos",
            "icon": "history_edu",
            "link": reverse_lazy("admin:accounts_studentacademicinfo_changelist"),
        },
        {
            "title": "Contact Infos",
            "icon": "badge",
            "link": reverse_lazy("admin:accounts_studentcontactinfo_changelist"),
        },
        {
            "title": "Parents Infos",
            "icon": "family_restroom",
            "link": reverse_lazy("admin:accounts_studentparentsinfo_changelist"),
        },
        {
            "title": "Health Infos",
            "icon": "health_and_safety",
            "link": reverse_lazy("admin:accounts_studenthealthinfo_changelist"),
        },
    ],
}


UNFOLD_TEACHER_PROFILE_NAVIGATION = {
    "title": "Teacher Management",
    "separator": True,
    "collapsible": True, 
    "items": [
        {
            "title": "Teacher Profiles",
            "icon": "co_present",
            "link": reverse_lazy("admin:accounts_teacherprofile_changelist"),
        },
        {
            "title": "Teacher Assignment",
            "icon": "co_present",
            "link": reverse_lazy("admin:accounts_teacherassignment_changelist"),
        },
        {
            "title": "Professional Infos",
            "icon": "work",
            "link": reverse_lazy("admin:accounts_teacherprofessionalinfo_changelist"),
        },
        {
            "title": "Contact Infos",
            "icon": "contact_phone",
            "link": reverse_lazy("admin:accounts_teachercontactinfo_changelist"),
        },
    ],     
}


UNFOLD_STAFF_PROFILE_NAVIGATION = {
    "title": "Staff Management",
    "separator": True,
    "collapsible": True,
    "items": [
        {
            "title": "Staff Profiles",
            "icon": "manage_accounts",
            "link": reverse_lazy("admin:accounts_staffprofile_changelist"),
        },
        {
            "title": "Staff Positions",
            "icon": "assignment_ind",
            "link": reverse_lazy("admin:accounts_staffposition_changelist"),
        },
        {
            "title": "Contact Infos",
            "icon": "import_contacts",
            "link": reverse_lazy("admin:accounts_staffcontactinfo_changelist"),
        },
    ],
}


UNFOLD_ADMIN_PROFILE_NAVIGATION = {
    "title": "Admin & Controls",
    "separator": True,
    "collapsible": True,
    "items": [
        {
            "title": "Admin Profiles",
            "icon": "admin_panel_settings",
            "link": reverse_lazy("admin:accounts_adminprofile_changelist"),
        },
        {
            "title": "Admin Contacts",
            "icon": "phone_in_talk",
            "link": reverse_lazy("admin:accounts_admincontactinfo_changelist"),
        },
    ],
}


UNFOLD_ONE_TIME_TOKEN_NAVIGATION = {
    "title": "One Time Token",
    "separator": True,
    "collapsible": True,
    "items": [
        { 
            "title": "One Time Token",
            "icon": "token",
            "link": reverse_lazy("admin:accounts_onetimetoken_changelist")
        }
    ]
}
