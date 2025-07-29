from django.db import models
from apps.recipe_api.timestamp import BaseTimeStampModel
from django.core.validators import MinValueValidator

# Create your models here.
class Category(models.Model):
    """
    Represents a category for recipes (e.g., 'Dessert', 'Main Course', 'Breakfast').
    """
    name = models.CharField(max_length=100, unique=True)

    class Meta:
        verbose_name_plural = "Categories"

    def __str__(self):
        return self.name
    
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
    
class Ingredient(models.Model):
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

class Instruction(models.Model):
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
    description = models.TextField()

    class Meta:
        ordering = ['step_number']
        unique_together = ('recipe', 'step_number')

    def __str__(self):
        return f"Step {self.step_number} for {self.recipe.title}"
    