from rest_framework import serializers
from apps.recipes.models.cuisine import Cuisine

class SubcategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = Cuisine
        fields = ['id', 'name']