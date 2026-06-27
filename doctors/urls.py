from django.urls import path
from .views import *

urlpatterns = [

    path(
        "availability/",
        AvailabilityListCreateView.as_view(),
        name="availability",
    ),

    path(
        "availability/<int:pk>/",
        AvailabilityUpdateDeleteView.as_view(),
        name="availability-update",
    ),
]