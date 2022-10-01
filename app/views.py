from django.contrib.auth import get_user_model
from rest_framework import viewsets
from app.serializers import UserSerializer
# Create your views here.


class UserViewSet(viewsets.ModelViewSet):
    User = get_user_model()
    queryset = User.objects.all()
    serializer_class = UserSerializer
