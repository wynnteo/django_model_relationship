from django.contrib.auth import get_user_model
from rest_framework import serializers
from .models import Detail, UserProfile, Account, Product, Order, Detail
from django.db import transaction


class AccountSerializer(serializers.ModelSerializer):
    class Meta:
        model = Account
        fields = (
            "id",
            "account_number",
            "account_type",
            "open_date",
            "balance",
            "user",
        )


class UserProfileSerializer(serializers.ModelSerializer):
    class Meta:
        model = UserProfile
        fields = ("id", "address", "dob", "mobile")


class UserSerializer(serializers.ModelSerializer):
    profile = UserProfileSerializer(many=False)
    accounts = AccountSerializer(many=True, required=False)

    class Meta:
        User = get_user_model()
        model = User
        fields = (
            "id",
            "first_name",
            "last_name",
            "email",
            "password",
            "profile",
            "accounts",
        )
        extra_kwargs = {"password": {"write_only": True, "required": True}}

    def create(self, validated_data):
        User = get_user_model()
        profile_data = validated_data.pop("profile")
        user = User.objects.create_user(**validated_data)
        UserProfile.objects.create(user=user, **profile_data)
        return user


# class ProductSerializer(serializers.ModelSerializer):
#     class Meta:
#         model = Product
#         fields = ('id', 'name', 'price', 'sku')

# class OrderSerializer(serializers.ModelSerializer):
#     # To return products object instead of id
#     products = ProductSerializer(read_only=True, many=True)
#     class Meta:
#         model = Order
#         fields = ('id', 'order_date', 'status', 'products')


class ProductSerializer(serializers.ModelSerializer):
    class Meta:
        model = Product
        fields = ("id", "name", "price", "sku")


class DetailSerializer(serializers.ModelSerializer):
    product = ProductSerializer(many=False)

    class Meta:
        model = Detail
        fields = ("id", "product", "quantity")


class OrderSerializer(serializers.ModelSerializer):
    products = DetailSerializer(source="detail_set", read_only=True, many=True)

    class Meta:
        model = Order
        fields = ("id", "order_date", "status", "products")

    @transaction.atomic
    def create(self, validated_data):
        order = Order.objects.create(**validated_data)
        if "products" in self.initial_data:
            products = self.initial_data.get("products")
            for product in products:
                id = product.get("id")
                quantity = product.get("quantity")
                product = Product.objects.get(pk=id)
                Detail(order=order, product=product, quantity=quantity).save()
        order.save()
        return order
