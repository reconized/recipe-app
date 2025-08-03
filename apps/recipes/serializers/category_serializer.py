import bleach
from rest_framework import serializers
from apps.recipes.models.category import Category

class CategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = Category
        fields = '__all__'