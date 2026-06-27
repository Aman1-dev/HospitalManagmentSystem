from django.db import models
from accounts.models import User


class Availability(models.Model):

    doctor = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        limit_choices_to={"role": "doctor"}
    )

    start_time = models.DateTimeField()

    end_time = models.DateTimeField()

    is_booked = models.BooleanField(default=False)

    def __str__(self):
        return f"{self.doctor.username} {self.start_time}"