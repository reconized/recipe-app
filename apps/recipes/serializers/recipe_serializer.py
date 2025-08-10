import bleach
from rest_framework import serializers
from apps.recipes.models.recipe import Recipe
from apps.recipes.models.category import Category
from apps.recipes.serializers.instruction_serializer import InstructionSerializer
from apps.recipes.serializers.ingredient_serializer import IngredientSerializer
from apps.recipes.serializers.category_serializer import CategorySerializer
from apps.recipes.serializers.user_serializer import UserSerializer
from apps.recipes.validators import validate_no_profanity

class RecipeSerializer(serializers.ModelSerializer):
    category_id = serializers.PrimaryKeyRelatedField(
        queryset=Category.objects.all(), source='category', write_only=True, required=False
    )
    instructions = InstructionSerializer(many=True, read_only=True)
    ingredients = IngredientSerializer(many=True, read_only=True)
    category = CategorySerializer(read_only=True)

    def validate_title(self, attrs):
        validate_no_profanity(attrs)
        return attrs
    
    def validate_description(self, attrs):
        if attrs:
            allowed_tags = list(bleach.sanitizer.ALLOWED_TAGS)
            allowed_tags.extend(['p', 'strong', 'em', 'br'])
            allowed_tags = set(allowed_tags)
            sanitized_attrs = bleach.clean(attrs, tags=allowed_tags, attributes={})
            if not sanitized_attrs.strip() and attrs.strip():
                raise serializers.ValidationError('Description contains only invalid HTML and was removed.')
            return sanitized_attrs
        return attrs
    
    def validate(self, attrs):
        if attrs.get('prep_time', 0) > 360 and attrs.get('cook_time', 0 < 10):
            raise serializers.ValidationError('Prep time seems disproportionately long compared to cook time.')
        return attrs

    class Meta:
        model = Recipe
        fields = [
            'id', 'category', 'category_id', 'title', 'prep_time', 'cook_time', 'servings', 
            'ingredients', 'instructions', 'created_at', 'updated_at'
        ]
        read_only_fields = ['created_at', 'updated_at']
