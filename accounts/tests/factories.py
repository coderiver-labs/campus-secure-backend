
from accounts.models import TeacherProfile, TeacherAssignment, StudentProfile

# factory
import factory
from factory.django import DjangoModelFactory

# import test utils 
from accounts.tests.users import TeacherUserFactory, StudentUserFactory
from accounts.tests.users import StudentUserFactory

# import factories
from school.tests.factories import StudentClassFactory, SubjectFactory


# Teacher Profile
class TeacherProfileFactory(DjangoModelFactory):
    class Meta:
        model = TeacherProfile
    user = factory.SubFactory(TeacherUserFactory)


# teacher Assignment
class TeacherAssignmentFactory(DjangoModelFactory):
    class Meta:
        model = TeacherAssignment

    teacher = factory.SubFactory(TeacherProfileFactory)
    student_class = factory.SubFactory(StudentClassFactory)
    subject = factory.SubFactory(SubjectFactory)





"""_______________ User Profile_____________"""
class StudentProfileFactory(DjangoModelFactory):
    class Meta:
        model = StudentProfile
    user = factory.SubFactory(StudentProfile)

from accounts.models import StudentAcademicInfo, StudentContactInfo, StudentHealthInfo, StudentParentsInfo
class StudentAcademicInfoFactory(DjangoModelFactory):
    class Meta:
        model = StudentAcademicInfo
    student = factory.SubFactory(StudentProfileFactory)
