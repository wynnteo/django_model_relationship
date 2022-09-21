from django.contrib.auth.models import User
from rest_framework import viewsets
from app.serializers import UserSerializer
# Create your views here.


class UserViewSet(viewsets.ModelViewSet):
    serializer_class = UserSerializer
    queryset = User.objects.all()
