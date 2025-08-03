from rest_framework import serializers
from apps.recipes.models.ingredient import Ingredient

class IngredientSerializer(serializers.ModelSerializer):
    class Meta:
        model = Ingredient
        fields = ['id', 'name', 'quantity', 'unit']