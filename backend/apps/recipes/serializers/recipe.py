from rest_framework import serializers
from apps.recipes.models.recipe import Recipe
from apps.recipes.models.cuisine import Cuisine
from apps.recipes.serializers.ingredient_read import IngredientReadSerializer
from apps.recipes.serializers.instruction_read import InstructionReadSerializer

class RecipeSerializer(serializers.ModelSerializer):
    category_name = serializers.CharField(source="category.name", read_only=True)
    cuisines = serializers.SlugRelatedField(
        many=True, read_only=True, slug_field="name"
    )

    cuisine_ids = serializers.PrimaryKeyRelatedField(
        many=True, source="cuisines", queryset=Cuisine.objects.all(), write_only=True
    )
    user = serializers.PrimaryKeyRelatedField(read_only=True)

    class Meta:
        model = Recipe
        fields = [
            "id", "user", "title", "description", 
            "prep_time", "cook_time", "servings",
            "category", "category_name", 
            "cuisines", "cuisine_ids",
            "total_time",
            ]
        
        def create(self, validated_data):
            cuisines = validated_data.pop("cuisines", [])
            recipe = Recipe.objects.create(**validated_data)
            if cuisines:
                recipe.cuisines.set(cuisines)
            return recipe
        
        def update(self, instance, validated_data):
            cuisines = validated_data.pop("cuisines", None)
            for attr, value in validated_data.items():
                setattr(instance, attr, value)
            instance.full_clean()
            instance.save()
            if cuisines is not None:
                instance.cuisines.set(cuisines)
            return instance
        
class RecipeDetailSerializer(RecipeSerializer):
    ingredients = IngredientReadSerializer(many=True, read_only=True)
    instructions = InstructionReadSerializer(many=True, read_only=True)

    class Meta(RecipeSerializer.Meta):
        fields = RecipeSerializer.Meta.fields + ["ingredients", "instructions"]
        read_only_fields = RecipeSerializer.Meta.fields + ["ingredients", "instructions"]