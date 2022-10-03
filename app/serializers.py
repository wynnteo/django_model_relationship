from django.contrib.auth import get_user_model
from rest_framework import serializers
from .models import UserProfile, Account


class AccountSerializer(serializers.ModelSerializer):
    class Meta:
        model = Account
        fields = ('id', 'account_number',
                  'account_type', 'open_date', 'balance', 'user')


class UserProfileSerializer(serializers.ModelSerializer):
    class Meta:
        model = UserProfile
        fields = ('id', 'address', 'dob', 'mobile')


class UserSerializer(serializers.ModelSerializer):
    profile = UserProfileSerializer(many=False)
    accounts = AccountSerializer(many=True)

    class Meta:
        User = get_user_model()
        model = User
        fields = ('id', 'first_name', 'last_name',
                  'email', 'password', 'profile', 'accounts')
        extra_kwargs = {'password': {'write_only': True, 'required': True}}

    def create(self, validated_data):
        User = get_user_model()
        profile_data = validated_data.pop('profile')
        user = User.objects.create_user(**validated_data)
        UserProfile.objects.create(user=user, **profile_data)
        return user
