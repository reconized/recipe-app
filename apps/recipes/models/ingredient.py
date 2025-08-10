from django.db import models
from django.core.exceptions import ValidationError
from apps.recipes.models.recipe import Recipe
from apps.recipes.timestamp import BaseTimeStampModel
from apps.recipes.constants import UNIT_CHOICES
from apps.recipes.templatetags.filters import fraction_to_unicode
from apps.recipes.validators import (
    validate_no_profanity, validate_quantity_format, validate_quantity
)

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
    quantity = models.CharField(
        max_length=20,
        help_text="Enter a number or fraction like '1/2' or '2 1/2'",
        validators=[validate_quantity_format, validate_quantity]
    )
    unit = models.CharField(
        max_length=10, 
        choices=UNIT_CHOICES,
        blank=True, 
        null=True,
    )

    class Meta:
        unique_together = ('recipe', 'name')

    def clean(self):
        super().clean()
        self.name = self.name.strip()

    def save(self, *args, **kwargs):
        if self.quantity:
            self.quantity = fraction_to_unicode(self.quantity.strip())
        super().save(*args, **kwargs)

    def __str__(self):
        if self.unit:
            return f"{self.quantity} {self.unit or ''} {self.name}".strip()
        return f"{self.quantity} {self.name}"
