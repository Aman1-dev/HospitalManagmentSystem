from django.urls import path
from .views import RegisterView, DoctorListView

from rest_framework_simplejwt.views import (
    TokenObtainPairView,
    TokenRefreshView,
)

urlpatterns = [

    path("signup/", RegisterView.as_view()),

    path("login/", TokenObtainPairView.as_view()),

    path("refresh/", TokenRefreshView.as_view()),

    path("doctors/", DoctorListView.as_view()),

]