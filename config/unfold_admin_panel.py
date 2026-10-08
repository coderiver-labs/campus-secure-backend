from django.urls import reverse_lazy

# import navigation
from accounts.unfold_navigation import (
    UNFOLD_USERS_NAVIGATION,
    UNFOLD_STUDENT_PROFILE_NAVIGATION,
    UNFOLD_TEACHER_PROFILE_NAVIGATION,
    UNFOLD_STAFF_PROFILE_NAVIGATION,
    UNFOLD_ADMIN_PROFILE_NAVIGATION,
    UNFOLD_ONE_TIME_TOKEN_NAVIGATION
)
from school.unfold_navigation import SCHOOL_NAVIGATION
from audit.unfold_navigation import AUDIT_NAVIGATION
from exams.unfold_navigation import EXAMS_NAVIGATION
from payment.unfold_navigation import PAYMENT_NAVIGATION



# UNFOLD Config

UNFOLD = {
    "SITE_TITLE": "Campus Secure Admin",
    "SITE_HEADER": "Campus Secure Backend",
    
    "DASHBOARD_CALLBACK": "config.dashboard.dashboard_callback", 
    "SITE_TITLE": "School-Management",
    "SITE_HEADER": "School Management",
    "SITE_FAVICONS": [
        {
            "rel": "icon",
            "type": "image/svg",  # টাইপ png করা হলো
            "href": "/static/icon/favicon.svg",  # ফাইলের নাম icon.png করা হলো
        },
    ],
    
    "SIDEBAR": {
        "show_search": True,
        "show_all_applications": False,
                
        "navigation": [
            {
                "items": [
                    {
                        "title": "Dashboard",
                        "icon": "dashboard",
                        "link": reverse_lazy("admin:index"),
                    },
                ],
            },
            
            # Accounts models admin
            UNFOLD_USERS_NAVIGATION,
            UNFOLD_STUDENT_PROFILE_NAVIGATION,
            UNFOLD_TEACHER_PROFILE_NAVIGATION,
            UNFOLD_STAFF_PROFILE_NAVIGATION,
            UNFOLD_ADMIN_PROFILE_NAVIGATION,

            # other apps
            SCHOOL_NAVIGATION,
            EXAMS_NAVIGATION,
            AUDIT_NAVIGATION,

            # SUBSCRIPTION_NAVIGATION,
            PAYMENT_NAVIGATION,

            # one time token 
            UNFOLD_ONE_TIME_TOKEN_NAVIGATION,
        ],
    }
}
