from django.db import models
from apps.recipes.timestamp import BaseTimeStampModel

# Create your models here.
class Category(BaseTimeStampModel):
    """
    Represents a category for recipes (e.g., 'Dessert', 'Main Course', 'Breakfast').
    """
    name = models.CharField(max_length=100, unique=True)

    class Meta:
        verbose_name_plural = "Categories"

    def __str__(self):
        return self.name