from django.db import models
from apps.recipes.models.recipe import Recipe
from apps.recipes.timestamp import BaseTimeStampModel

class Ingredient(BaseTimeStampModel):
    """
    Represents an ingredient for a specific recipe.
    """
    recipe = models.ForeignKey(
        Recipe,
        on_delete=models.CASCADE,
        related_name='ingredients'
    )
    name = models.CharField(max_length=100)
    quantity = models.DecimalField(max_digits=6, decimal_places=2)
    unit = models.CharField(max_length=50, blank=True, null=True)

    class Meta:
        unique_together = ('recipe', 'name')

    def __str__(self):
        return f"{self.quantity} {self.unit or ''} {self.name} for {self.recipe.title}"
