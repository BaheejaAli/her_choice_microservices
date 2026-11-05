from rest_framework import generics
from .models import AppUser
from .serializers import UserSerializer


class UserListCreateView(generics.ListCreateAPIView):
    queryset = AppUser.objects.all().order_by("id")
    serializer_class = UserSerializer


class UserDetailView(generics.RetrieveAPIView):
    queryset = AppUser.objects.all()
    serializer_class = UserSerializer