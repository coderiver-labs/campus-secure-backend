from django.urls import reverse

# DRF
from rest_framework.test import APIClient
from rest_framework.response import Response

#import pytest
import pytest

# import factories
from accounts.tests.factories import TeacherAssignmentFactory, TeacherProfileFactory
from school.tests.factories import SubjectFactory, StudentClassFactory

# import models 
from accounts.models import CustomUser, TeacherProfile, TeacherAssignment
from school.models import StudentClass, Subject


# import test user
from accounts.tests.users import AdminUserFactory
from accounts.tests.users import TeacherUserFactory


# create teacher test case




# pytestmark = pytest.mark.django_db
"""
@pytest.mark.django_db
class TestTeacherAssignmentAPI:
    def test_teacher_can_view_own_assignment(self, api_client: APIClient, teacher_profile_1: TeacherProfile, teacher_profile_2: TeacherProfile):

        TeacherAssignmentFactory(teacher=teacher_profile_1)
        TeacherAssignmentFactory(teacher=teacher_profile_2)


        api_client.force_authenticate(user=teacher_profile_1.user)

        url = reverse("teacher-assignment-list")
        response: Response = api_client.get(url)

        assert response.status_code == 200
        assert len(response.data["results"]) == 1
        assert response.data["results"][0]["teacher"]["uuid"] == str(teacher_profile_1.uuid)


    def test_admin_can_list_assignments(self, api_client: APIClient, teacher_profile_1, teacher_profile_2):

        TeacherAssignmentFactory(teacher=teacher_profile_1)
        TeacherAssignmentFactory(teacher=teacher_profile_2)

        url = reverse("teacher-assignment-list")
        user: CustomUser = AdminUserFactory()

        api_client.force_authenticate(user=user)

        response: Response = api_client.get(url)

        assert response.status_code == 200
        assert len(response.data["results"]) == 2


    def test_admin_can_create_assignment(self, api_client: APIClient):

        user = AdminUserFactory()
        url = reverse("teacher-assignment-list")
        teacher_profile = TeacherProfileFactory()
        subject = SubjectFactory()
        student_class = StudentClassFactory()

        payload = {
            "teacher": teacher_profile.uuid,
            "subject": subject.uuid,
            "student_class": student_class.uuid
        }
        api_client.force_authenticate(user=user)
        response: Response = api_client.post(path=url, data=payload, format="json")
        # print(response.data)
        # db test
        assert TeacherAssignment.objects.count() == 1

        assert response.status_code == 201
        assert response.data["teacher"] == teacher_profile.uuid
        assert response.data["subject"] == subject.uuid
        assert response.data["student_class"] == student_class.uuid


    def test_teacher_cannot_create_assignment(self, api_client: APIClient, teacher_profile_1):

        TeacherAssignmentFactory(teacher=teacher_profile_1)

        user = TeacherUserFactory()
        
        url = reverse("teacher-assignment-list")
        teacher_profile = TeacherProfileFactory()
        subject = SubjectFactory()
        student_class = StudentClassFactory()
        
        payload = {
            "teacher": teacher_profile.uuid,
            "subject": subject.uuid,
            "student_class": student_class.uuid
        }
        api_client.force_authenticate(user=user)
        response: Response = api_client.post(path=url, data=payload, format="json")
        
        # db test
        assert TeacherAssignment.objects.count() == 1
        assert response.status_code == 403


    def test_duplicate_assignment_returns_400(self, api_client: APIClient, teacher_profile_1: TeacherProfile):

        # create teacher assignment with teacher_profile_1
        assignment = TeacherAssignmentFactory(teacher=teacher_profile_1)        
        print(assignment)
        user = AdminUserFactory()
        url = reverse("teacher-assignment-list")

        # akta teacher ekta class ar ekoi subject 2bar add hobena
        payload = {
            "teacher": teacher_profile_1.uuid, # ai teacher already nirdito class r subject a ase tai amar abar same subjet r same class diye add korar cesta korbo 
            "subject": assignment.subject.uuid, 
            "student_class": assignment.student_class.uuid
        }
        api_client.force_authenticate(user=user) 
        response: Response = api_client.post(path=url, data=payload, format="json")

        # check db 
        assert TeacherAssignment.objects.count() == 1
        assert response.status_code == 400


        # ekjon teacher caile ekta class ar akadhik subject a porate parbe. 
        subject = SubjectFactory()
        payload = {
            "teacher": teacher_profile_1.uuid,
            "subject": subject.uuid,
            "student_class": assignment.student_class.uuid
        }
        response: Response = api_client.post(path=url, data=payload, format="json")

        assert response.status_code == 201
        assert response.data["student_class"] == assignment.student_class.uuid
        assert response.data["subject"] == subject.uuid



    # akhne admin and teacher ar 2ta ek sathe test kora hoyese 
    def test_admin_can_update_assignment(self, api_client: APIClient, teacher_profile_1: TeacherProfile):
        user = AdminUserFactory()

        assignment = TeacherAssignmentFactory(teacher=teacher_profile_1)
        subject = SubjectFactory()
        student_class = StudentClassFactory()
        
        url = reverse("teacher-assignment-detail", kwargs={"uuid": assignment.uuid})
        payload = {
            "subject": subject.uuid,
            "student_class": student_class.uuid
        }
        api_client.force_authenticate(user=user)
        response: Response = api_client.patch(path=url, data=payload, format="json")
        
        # update_assignment = TeacherAssignment.objects.get(teacher=teacher_profile_1) # ata ar poriborte refresh_from_db use kora hoyese
        assignment.refresh_from_db() # ata dile assignment ar moddhe je data ase seta refresh hoye jabe amader new data te

        assert TeacherAssignment.objects.count() == 1
        assert response.status_code == 200
        assert response.data["subject"] == subject.uuid

        assert assignment.subject == subject
        assert assignment.student_class == student_class


    def test_admin_can_delete_assignment(self, api_client: APIClient, teacher_profile_1: TeacherProfile):
        user = AdminUserFactory()
        assignment = TeacherAssignmentFactory(teacher=teacher_profile_1)

        url = reverse("teacher-assignment-detail", kwargs={"uuid": assignment.uuid})
        api_client.force_authenticate(user=user)
        response: Response = api_client.delete(path=url)

        assert TeacherAssignment.objects.count() == 0
        assert response.status_code == 200

        
    def test_teacher_cannot_delete_assignment(self, api_client: APIClient, teacher_profile_1):
        user = TeacherUserFactory()
        assignment = TeacherAssignmentFactory(teacher=teacher_profile_1)

        url = reverse("teacher-assignment-detail", kwargs={"uuid": assignment.uuid})
        api_client.force_authenticate(user=user)
        response: Response = api_client.delete(path=url) 

        assert TeacherAssignment.objects.count() == 1
        assert response.status_code == 403

"""








