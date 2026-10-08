SPECTACULAR_SETTINGS = {
    "TITLE": "Campus Secure API",
    "DESCRIPTION": (
        "Campus Secure is a school management and administration backend API "
        "built with Django REST Framework. The system provides APIs for "
        "managing user accounts, students, teachers, staff, administrators, "
        "academic classes, subjects, exams, exam candidates, marks, "
        "subscriptions, payments, documents, and audit logs. "
        "\n\n"
        "The API implements role-based access control for administrators, "
        "staff, teachers, and students, with policy-based authorization "
        "and object-level access control where required. "
        "\n\n"
        "The system also includes authentication using secure HTTP cookies "
        "and CSRF protection, API filtering, searching, ordering, audit "
        "logging, payment processing, and background task support. "
        "\n\n"
        "This documentation describes the available API endpoints, "
        "request and response schemas, authentication requirements, "
        "query parameters, and supported operations."
    ),
    "VERSION": "1.0.0",
    "SERVE_INCLUDE_SCHEMA": False,

    "SWAGGER_UI_DIST": "SIDECAR",
    "SWAGGER_UI_FAVICON_HREF": "SIDECAR",
    "REDOC_DIST": "SIDECAR",

    "TAGS": [
        {
            "name": "Authentication",
            "description": (
                "APIs for user authentication, including login, logout, token management, "
                "CSRF protection, password recovery, and authentication-related operations."
            ),
        },
        {
            "name": "Accounts",
            "description": (
                "APIs for managing user accounts, including user information, account updates, "
                "password changes, and account-related operations."
            ),
        },
        {
            "name": "Profile",
            "description": (
                "APIs for managing user profile information and profile pictures, including "
                "secure access to protected profile files."
            ),
        },
        {
            "name": "Student Profile & Academic",
            "description": (
                "APIs for managing student profile and academic information, "
                "including student identity, academic details, class-related "
                "information, and other core student records."
            ),
        },
        {
            "name": "Student Additional Information",
            "description": (
                "APIs for managing additional student information, including "
                "parent or guardian details, contact information, and health-related records."
            ),
        },
        {
            "name": "Teacher Assignments",
            "description": (
                "APIs for managing teacher assignments, including the relationship between "
                "teachers, student classes, and subjects."
            ),
        },
        {
            "name": "Teacher Related",
            "description": (
                "APIs for managing teacher-related information, profiles, assignments, "
                "and other operations associated with teachers."
            ),
        },
        {
            "name": "Staff Related",
            "description": (
                "APIs for managing staff-related information, profiles, positions, "
                "and other operations associated with school staff."
            ),
        },
        {
            "name": "Admin Related",
            "description": (
                "APIs for administrator-related operations, including administrative "
                "information and privileged school management functionality."
            ),
        },

        {
            "name": "Exam Management",
            "description": (
                "APIs for creating and managing exams, including exam information, "
                "academic year, status, schedule, activation, and exam lifecycle operations."
            ),
        },
        {
            "name": "Exam Classes",
            "description": (
                "APIs for managing classes associated with exams, including the student "
                "classes participating in specific exams."
            ),
        },
        {
            "name": "Exam Subjects",
            "description": (
                "APIs for managing subjects included in exams, including exam subject "
                "configuration, full marks, pass marks, and subject-specific exam settings."
            ),
        },
        {
            "name": "Exam Candidates & Marks",
            "description": (
                "APIs for managing exam candidates and student marks, including candidate "
                "status, mark entry, completed candidates, and exam result-related data."
            ),
        },

        {
            "name": "Payments",
            "description": (
                "APIs for managing student school fee payment records, including payment "
                "creation, retrieval, updates, and payment-related administrative operations."
            ),
        },
        {
            "name": "Payment Checkout",
            "description": (
                "Public APIs for viewing available school fee plans and creating payment "
                "checkout sessions for students through the payment system."
            ),
        },
        {
            "name": "Payment Callback",
            "description": (
                "APIs for handling payment callback flows, including successful and "
                "cancelled payment responses after the checkout process."
            ),
        },
        {
            "name": "Stripe Webhook",
            "description": (
                "API for securely receiving and processing Stripe webhook events, including "
                "verification of webhook signatures and completed checkout sessions."
            ),
        },

        {
            "name": "Subjects",
            "description": (
                "APIs for managing school subjects, including subject names, codes, "
                "descriptions, active status, and subject-related operations."
            ),
        },
        {
            "name": "Class Levels",
            "description": (
                "APIs for managing school class levels, including monthly fees and "
                "the subjects associated with each class level."
            ),
        },
        {
            "name": "Sections",
            "description": (
                "APIs for managing school sections used to organize students within "
                "classes and maintain section-related information."
            ),
        },
        {
            "name": "Student Classes",
            "description": (
                "APIs for managing student classes by associating class levels with "
                "their corresponding sections and maintaining class-related information."
            ),
        },
        {
            "name": "Integrations",
            "description": (
                "APIs for integrating Campus Secure with external services and platforms, "
                "including error monitoring, notifications, webhooks, "
                "and other third-party system integrations."
            ),
        },
        {
            "name": "Audit Logs",
            "description": (
                "APIs for tracking and reviewing system activity, including user actions, "
                "created records, updated records, deleted records, and other auditable changes."
            ),
        },
        {
            "name": "Test And Error",
            "description": (
                "Test and development APIs for validating application behavior, including "
                "error responses, intentional delays, slow database queries, and other test scenarios."
            ),
        },
        {
            "name": "About",
            "description": (
                "APIs for managing and retrieving school about information."
            ),
        },
    ],
}