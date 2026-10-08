from django.contrib.auth.hashers import make_password

# factory
import factory
from factory.django import DjangoModelFactory

# import models 
from accounts.models import CustomUser


# create base test factory hare


class BaseUserFactory(DjangoModelFactory):
    class Meta:
        model = CustomUser

    first_name = "Test"
    last_name = "User"
    email = factory.Sequence(lambda n: f"user{n}@test.com")
    is_active = True
    is_verified = True


