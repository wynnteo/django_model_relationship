from django.contrib.auth import get_user_model
from rest_framework import viewsets
from app.serializers import UserSerializer
from .models import Account
from app.serializers import AccountSerializer
# Create your views here.


class UserViewSet(viewsets.ModelViewSet):
    User = get_user_model()
    queryset = User.objects.all()
    serializer_class = UserSerializer


class AccountViewSet(viewsets.ModelViewSet):
    queryset = Account.objects.all()
    serializer_class = AccountSerializer
