from django.urls import reverse_lazy



# create your unfold admin config




EXAMS_NAVIGATION = {
    "title": "Exams Management",
    "icon": "assignment",
    "separator": True,
    "collapsible": True,
    "items": [
        {
            "title": "Exam",
            "icon": "assignment",
            "link": reverse_lazy("admin:exams_exam_changelist"),
        },
        {
            "title": "Exam Classes",
            "icon": "class",
            "link": reverse_lazy("admin:exams_examclass_changelist"),
        },
        {
            "title": "Exam Subjects",
            "icon": "menu_book",
            "link": reverse_lazy("admin:exams_examsubject_changelist"),
        },
        {
            "title": "Student Marks",
            "icon": "grading",
            "link": reverse_lazy("admin:exams_studentmark_changelist"),
        },
    ],
}