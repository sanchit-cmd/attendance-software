from django.db import models
from django.contrib.auth.models import (
    AbstractBaseUser,
    PermissionsMixin,
)
from .managers import UserManager

# Create your models here.


class UserRole(models.TextChoices):
    ADMIN = "ADMIN", "Admin"
    TEACHER = "TEACHER", "Teacher"
    STUDENT = "STUDENT", "Student"


class User(AbstractBaseUser, PermissionsMixin):

    phone = models.CharField(max_length=20, unique=True)
    name = models.CharField(max_length=100, blank=True)
    role = models.CharField(
        max_length=20, choices=UserRole.choices, default=UserRole.STUDENT
    )

    is_active = models.BooleanField(default=True)
    is_staff = models.BooleanField(default=False)
    objects = UserManager()

    USERNAME_FIELD = "phone"

    def __str__(self):
        if self.name:
            return f"{self.name} ({self.phone})"
        return self.phone
