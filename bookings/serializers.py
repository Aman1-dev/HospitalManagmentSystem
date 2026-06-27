from rest_framework import serializers
from .models import Booking


class BookingSerializer(serializers.ModelSerializer):

    patient_name = serializers.CharField(
        source="patient.username",
        read_only=True
    )

    doctor_name = serializers.CharField(
        source="availability.doctor.username",
        read_only=True
    )

    start_time = serializers.DateTimeField(
        source="availability.start_time",
        read_only=True
    )

    end_time = serializers.DateTimeField(
        source="availability.end_time",
        read_only=True
    )

    class Meta:
        model = Booking
        fields = [
            "id",
            "patient",
            "patient_name",
            "doctor_name",
            "availability",
            "start_time",
            "end_time",
            "booked_at",
        ]
        read_only_fields = (
            "patient",
            "booked_at",
        )