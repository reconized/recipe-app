from rest_framework import serializers
from apps.recipes.models.recipe import Recipe
from apps.recipes.models.category import Category
from apps.recipes.serializers.instruction_serializer import InstructionSerializer
from apps.recipes.serializers.ingredient_serializer import IngredientSerializer
from apps.recipes.serializers.category_serializer import CategorySerializer

class RecipeSerializer(serializers.ModelSerializer):
    category_id = serializers.PrimaryKeyRelatedField(
        queryset=Category.objects.all(), source='category', write_only=True, required=False
    )

    instructions = InstructionSerializer(many=True, read_only=True)
    ingredients = IngredientSerializer(many=True, read_only=True)
    category = CategorySerializer(read_only=True)

    class Meta:
        model = Recipe
        fields = [
            'id', 'category_id', 'title', 'prep_time', 'cook_time', 'servings', 
            'ingredients', 'instructions', 'created_at', 'updated_at'
        ]
        read_only_fields = ['created_at', 'updated_at']
