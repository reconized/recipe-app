import bleach
from rest_framework import serializers
from django.contrib.auth.models import User
from apps.recipe_api.models.category import Category

class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['id', 'username', 'email']

class CategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = Category
        fields = '__all__'