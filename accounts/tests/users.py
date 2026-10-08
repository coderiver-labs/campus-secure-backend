
from accounts.tests.base_user import BaseUserFactory

# 


class StudentUserFactory(BaseUserFactory):
    role = "student"

class TeacherUserFactory(BaseUserFactory):
    role = "teacher"


class AdminUserFactory(BaseUserFactory):
    role = "admin"

