from django.contrib.auth.models import AbstractUser
from django.db import models


class User(AbstractUser):

    ROLE_CHOICES = (
        ("doctor", "Doctor"),
        ("patient", "Patient"),
    )

    role = models.CharField(
        max_length=20,
        choices=ROLE_CHOICES
    )

    specialization = models.CharField(
        max_length=100,
        blank=True
    )

    phone = models.CharField(
        max_length=15,
        blank=True
    )

    address = models.TextField(
        blank=True
    )

    def __str__(self):
        return f"{self.username} ({self.role})"