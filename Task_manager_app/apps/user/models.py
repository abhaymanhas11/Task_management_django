from typing import Any
from django.db import models
from django.contrib.auth.models import AbstractUser, BaseUserManager
from apps.utils.enum import UserType


class User_manager(BaseUserManager):
    use_in_migrations = True

    def create_user(self, email, password=None, confirm_password=None, **extra_fields):
        if not email:
            raise ValueError("The email field must e required")
        email = self.normalize_email(email)
        user = self.model(email=email, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_admin(self, email, password, **extra_fields):
        extra_fields.setdefault("is_staff", True)
        extra_fields.setdefault("is_superuser", False)
        extra_fields.setdefault("is_active", True)
        return self.create_user(email, password, **extra_fields)

    def create_superuser(self, email, password, **extra_fields):
        extra_fields.setdefault("is_staff", True)
        extra_fields.setdefault("is_superuser", True)
        extra_fields.setdefault("is_active", True)
        if extra_fields.get("is_staff") is not True:
            raise ValueError("Superuser must have is_staff=True")
        if extra_fields.get("is_superuser") is not True:
            raise ValueError("Superuser must have is_superuser=True")
        return self.create_user(email, password, **extra_fields)


class User(AbstractUser):
    username = models.CharField(max_length=150)
    first_name = models.CharField(max_length=150)
    last_name = models.CharField(max_length=150)
    email = models.EmailField(unique=True)
    user_type = models.CharField(max_length=150, choices=UserType.choices())
    is_staff = models.BooleanField(default=False)
    is_superuser = models.BooleanField(default=False)

    is_active = models.BooleanField(
        default=False,
    )

    objects = User_manager()

    USERNAME_FIELD = "email"
    REQUIRED_FIELDS = ["user_type"]

    def __str__(self):
        return self.email
