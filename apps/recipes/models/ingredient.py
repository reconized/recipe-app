from django.db import models
from apps.recipes.models.recipe import Recipe
from apps.recipes.timestamp import BaseTimeStampModel
from apps.recipes.constants import UNIT_CHOICES
from apps.recipes.validators import validate_no_profanity

class Ingredient(BaseTimeStampModel):
    """
    Represents an ingredient for a specific recipe.
    """
    recipe = models.ForeignKey(
        Recipe,
        on_delete=models.CASCADE,
        related_name='ingredients'
    )
    name = models.CharField(max_length=100, validators=[validate_no_profanity])
    quantity = models.DecimalField(max_digits=6, decimal_places=2)
    unit = models.CharField(
        max_length=10, 
        choices=UNIT_CHOICES,
        blank=True, 
        null=True
    )

    class Meta:
        unique_together = ('recipe', 'name')

    def __str__(self):
        return f"{self.quantity} {self.get_unit_display() or ''} {self.name} for {self.recipe.title}"
