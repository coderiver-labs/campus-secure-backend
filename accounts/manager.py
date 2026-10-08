from django.contrib.auth.models import BaseUserManager
from django.contrib.auth.models import AbstractBaseUser


# create Manager hare



class UserManager(BaseUserManager):
    def create_user(self, email: str, password: str, role: str = "student", **extra_fields):
        if not email:
            raise ValueError("Email must be provided")

        if not password:
            raise ValueError("Password must be provided")

        email = self.normalize_email(email)

        user: AbstractBaseUser = self.model(email=email, role=role, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user


    def create_superuser(self, email: str, password: str, **extra_fields):
        extra_fields.setdefault("is_staff", True)
        extra_fields.setdefault("is_superuser", True)
        extra_fields.setdefault("is_verified", True)

        if extra_fields.get("is_staff") is not True:
            raise ValueError("Superuser must have is_staff=True")

        if extra_fields.get("is_superuser") is not True:
            raise ValueError("Superuser must have is_superuser=True")

        # Superuser does not belong to operational role logic
        return self.create_user(email=email, password=password, role="admin", **extra_fields )