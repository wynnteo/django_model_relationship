from django.contrib.auth import get_user_model
from rest_framework import viewsets
from .models import Account, Order, Product
from django.db import transaction
from rest_framework.response import Response
from app.serializers import (
    UserSerializer,
    AccountSerializer,
    OrderSerializer,
    ProductSerializer,
)

# Create your views here.


class UserViewSet(viewsets.ModelViewSet):
    User = get_user_model()
    queryset = User.objects.all()
    serializer_class = UserSerializer


class AccountViewSet(viewsets.ModelViewSet):
    queryset = Account.objects.all()
    serializer_class = AccountSerializer

    def transfer(self, request):
        try:
            user_a = request.POST.get("user_a")
            user_b = request.POST.get("user_b")
            amount = request.POST.get("amount")

            with transaction.atomic():
                user_a_obj = Account.objects.get(user=user_a)
                user_a_obj.balance -= int(amount)
                user_a_obj.save()

                # raise Exception

                user_b_obj = Account.objects.get(user=user_b)
                user_b_obj.balance += int(amount)
                user_b_obj.save()

                return Response(
                    {"status": "success", "message": "Your amount is transfered."}
                )

        except Exception as e:
            print(e)
            return Response({"status": "failed", "message": "Something went wrong."})


class OrderViewSet(viewsets.ModelViewSet):
    queryset = Order.objects.all()
    serializer_class = OrderSerializer


class ProductViewSet(viewsets.ModelViewSet):
    queryset = Product.objects.all()
    serializer_class = ProductSerializer
