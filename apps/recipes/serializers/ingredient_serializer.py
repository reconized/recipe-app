import re
from rest_framework import serializers
from apps.recipes.models.ingredient import Ingredient
from apps.recipes.constants import UNIT_CHOICES
from apps.recipes.templatetags.filters import fraction_to_unicode

class IngredientSerializer(serializers.ModelSerializer):
    class Meta:
        model = Ingredient
        fields = '__all__'

    def validate_quantity(self, value):
        if not value or not value.strip():
            raise serializers.ValidationError('Quantity is required.')
        
        if not re.match(r'^[0-9\s/]+$', value):
            raise serializers.ValidationError(
                "Quantity can only contain numbers, spaces, and '/'."
            )
        
        try:
            total = 0.0
            parts = value.strip()
            for part in parts:
                if '/' in part:
                    num, denom = part.split('/')
                    total += float(num) / float(denom)
                else:
                    total += float(part)
            
            if total <= 0:
                raise serializers.ValidationError('Quantity must be greater than zero.')
        except (ValueError, ZeroDivisionError):
            raise serializers.ValidationError('Invalid quantity format.')
        
        return value

    def validate_unit(self, value):
        if value:
            valid_units = dict(UNIT_CHOICES)
            if value and value not in dict(UNIT_CHOICES):
                raise serializers.ValidationError('Invalid unit choice.')
        return value
    
    def to_representation(self, instance):
        rep = super().to_representation(instance)
        rep['quantity'] = fraction_to_unicode(rep['quantity']) if rep.get('quantity') else None
        return rep