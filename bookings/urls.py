from django.urls import path
from .views import *

urlpatterns = [

    path(
        "available/",
        AvailableSlotsView.as_view(),
        name="available-slots",
    ),

    path(
        "book/",
        BookAppointmentView.as_view(),
        name="book",
    ),

    path(
        "my-appointments/",
        MyAppointmentsView.as_view(),
        name="my-appointments",
    ),

    path(
        "doctor-bookings/",
        DoctorBookingsView.as_view(),
        name="doctor-bookings",
    ),
]