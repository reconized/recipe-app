from rest_framework import serializers
from apps.recipes.models.ingredient import Ingredient

class IngredientReadSerializer(serializers.ModelSerializer):
    class Meta:
        model = Ingredient
        fields = ["id", "name", "quantity", "unit"]
        read_only_fields = fields