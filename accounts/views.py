from rest_framework import generics
from .models import User
from .serializers import RegisterSerializer, DoctorSerializer


class RegisterView(generics.CreateAPIView):

    queryset = User.objects.all()
    serializer_class = RegisterSerializer


class DoctorListView(generics.ListAPIView):

    serializer_class = DoctorSerializer

    def get_queryset(self):
        return User.objects.filter(role="doctor")