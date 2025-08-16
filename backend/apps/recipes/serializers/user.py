from rest_framework import serializers
from djoser.serializers import UserCreateSerializer
from django.contrib.auth.models import User
from django.db import transaction
from apps.recipes.models.user_profile import Profile

class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['id', 'username', 'email', 'first_name', 'last_name']

class CustomUserCreateSerializer(UserCreateSerializer):
    display_name = serializers.CharField(
        write_only=True,
        required=False,
        allow_blank=True,
        max_length=50
    )

    class Meta(UserCreateSerializer.Meta):
        fields = UserCreateSerializer.Meta.fields + ('display_name',)
    
    @transaction.atomic
    def create(self, validated_data):
        display_name = validated_data.pop('display_name', '')
        user = super().create(validated_data)
        Profile.objects.create(user=user, display_name=display_name)
        return user