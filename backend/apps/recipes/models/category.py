from django.db import models
from apps.recipes.timestamp import BaseTimeStampModel
from apps.recipes.validators import validate_no_profanity

class Category(BaseTimeStampModel):
    """
    Represents a category for recipes (e.g., 'Dessert', 'Main Course', 'Breakfast').
    """
    name = models.CharField(max_length=100, unique=True, validators=[validate_no_profanity])

    class Meta:
        verbose_name_plural = "Categories"

    def __str__(self):
        return self.name