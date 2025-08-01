from django.db import models
from apps.recipe_api.models.category import Category
from apps.recipe_api.timestamp import BaseTimeStampModel
from django.core.validators import MinValueValidator
    
class Recipe(BaseTimeStampModel):
    """
    Represents a single recipe.
    """
    title = models.CharField(max_length=200)
    description = models.TextField(blank=True, null=True)
    prep_time_minutes = models.IntegerField(
        validators=[MinValueValidator(0)],
        help_text="Cooking time in minutes"
    )
    cook_time_minutes = models.IntegerField(
        validators=[MinValueValidator(0)],
        help_text="Cooking time in minutes"
    )
    servings = models.IntegerField(
        validators=[MinValueValidator(1)],
        help_text="Number of servings the recipe yields"
    )

    category = models.ForeignKey(
        Category, on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name='recipes'
    )

    def total_time(self):
        return self.prep_time_minutes + self.cook_time_minutes
    
    class Meta:
        ordering = ['title']

    def __str__(self):
        return self.title