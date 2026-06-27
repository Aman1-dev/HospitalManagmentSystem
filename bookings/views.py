from django.db import IntegrityError, transaction
import logging
import requests

from rest_framework import generics, status
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView

from accounts.permissions import IsDoctor, IsPatient
from doctors.models import Availability
from doctors.serializers import AvailabilitySerializer

from calendar_service.google_calendar import create_event

from .models import Booking
from .serializers import BookingSerializer

logger = logging.getLogger(__name__)


class BookAppointmentView(APIView):

    permission_classes = [IsAuthenticated, IsPatient]

    @transaction.atomic
    def post(self, request):

        availability_id = request.data.get("availability_id")

        if not availability_id:
            return Response(
                {"error": "Availability ID is required"},
                status=status.HTTP_400_BAD_REQUEST,
            )

        try:
            slot = Availability.objects.select_for_update().get(id=availability_id)
        except Availability.DoesNotExist:
            return Response(
                {"error": "Slot not found"},
                status=status.HTTP_404_NOT_FOUND,
            )

        if slot.is_booked:
            return Response(
                {"error": "Slot already booked"},
                status=status.HTTP_400_BAD_REQUEST,
            )

        # Mark slot as booked
        slot.is_booked = True
        slot.save()

        # Create booking (protect against races)
        try:
            booking = Booking.objects.create(
                patient=request.user,
                availability=slot,
            )
        except IntegrityError:
            # Likely Booking/OneToOne uniqueness violation due to concurrent requests
            slot.refresh_from_db(fields=["is_booked"])
            return Response(
                {"error": "Slot already booked"},
                status=status.HTTP_400_BAD_REQUEST,
            )

        # -----------------------------
        # Google Calendar Integration
        # -----------------------------
        try:
            create_event(
                doctor=slot.doctor.username,
                patient=request.user.username,
                start=slot.start_time,
                end=slot.end_time,
            )
        except Exception:
            logger.exception("Google Calendar Error")

        # -----------------------------
        # Email Service Integration
        # -----------------------------
        try:
            requests.post(
                "http://127.0.0.1:5000/send-email",
                json={
                    "email": request.user.email,
                    "subject": "Appointment Confirmation",
                    "message": (
                        f"Hello {request.user.username},\n\n"
                        f"Your appointment with Dr. {slot.doctor.username} "
                        f"has been confirmed.\n\n"
                        f"Date : {slot.start_time.date()}\n"
                        f"Time : {slot.start_time.strftime('%I:%M %p')} - "
                        f"{slot.end_time.strftime('%I:%M %p')}\n\n"
                        f"Thank you for choosing our hospital."
                    ),
                },
                timeout=5,
            )
        except Exception:
            logger.exception("Email Service Error")

        serializer = BookingSerializer(booking)

        return Response(
            serializer.data,
            status=status.HTTP_201_CREATED,
        )


class AvailableSlotsView(generics.ListAPIView):

    serializer_class = AvailabilitySerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        return Availability.objects.filter(is_booked=False)


class MyAppointmentsView(generics.ListAPIView):

    serializer_class = BookingSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        return Booking.objects.filter(patient=self.request.user)


class DoctorBookingsView(generics.ListAPIView):

    serializer_class = BookingSerializer
    permission_classes = [IsAuthenticated, IsDoctor]

    def get_queryset(self):
        return Booking.objects.filter(availability__doctor=self.request.user)

