
from rest_framework.test import APIClient

# import models
from accounts.tests.factories import TeacherProfileFactory

# import pytest
import pytest


# create fixture


@pytest.fixture
def teacher_profile_1():
    return TeacherProfileFactory()


@pytest.fixture
def teacher_profile_2():
    return TeacherProfileFactory()


def student_1():
    return ...