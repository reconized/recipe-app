from django.db import models
from apps.recipes.models.recipe import Recipe
from apps.recipes.timestamp import BaseTimeStampModel
from apps.recipes.validators import validate_no_profanity
from django.core.validators import MinValueValidator

class Instruction(BaseTimeStampModel):
    """
    Represents step-by-step instructions for a recipe.
    """
    recipe = models.ForeignKey(
        Recipe, 
        on_delete=models.CASCADE,
        related_name='instructions'
    )
    step_number = models.PositiveIntegerField(
        validators=[MinValueValidator(1)],
        help_text='Order of the instruction step'
    )
    description = models.TextField(validators=[validate_no_profanity])
    image = models.ImageField()

    class Meta:
        ordering = ['step_number']
        unique_together = ('recipe', 'step_number')

    def __str__(self):
        return f"Step {self.step_number} for {self.recipe.title}"