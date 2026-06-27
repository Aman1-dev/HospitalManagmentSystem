from rest_framework import serializers
from .models import Availability


class AvailabilitySerializer(serializers.ModelSerializer):

    doctor_name = serializers.CharField(
        source="doctor.username",
        read_only=True
    )

    class Meta:
        model = Availability
        fields = [
            "id",
            "doctor",
            "doctor_name",
            "start_time",
            "end_time",
            "is_booked"
        ]

        read_only_fields = (
            "doctor",
            "doctor_name",
            "is_booked",
        )