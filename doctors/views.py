from rest_framework import generics
from rest_framework.permissions import IsAuthenticated
from .models import Availability
from .serializers import AvailabilitySerializer
from accounts.permissions import IsDoctor


class AvailabilityListCreateView(generics.ListCreateAPIView):
    serializer_class = AvailabilitySerializer
    permission_classes = [IsAuthenticated, IsDoctor]

    def get_queryset(self):
        return Availability.objects.filter(doctor=self.request.user)

    def perform_create(self, serializer):
        serializer.save(doctor=self.request.user)


class AvailabilityUpdateDeleteView(generics.RetrieveUpdateDestroyAPIView):

    serializer_class = AvailabilitySerializer
    permission_classes = [IsAuthenticated, IsDoctor]

    def get_queryset(self):
        return Availability.objects.filter(
            doctor=self.request.user
        )