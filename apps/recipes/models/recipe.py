from django.db import models
from django.contrib.auth.models import User
from apps.recipes.models.category import Category
from apps.recipes.timestamp import BaseTimeStampModel
from django.core.validators import MinValueValidator
from apps.recipes.validators import validate_no_profanity
import bleach
    
class Recipe(BaseTimeStampModel):
    """
    Represents a single recipe.
    """
    user = models.ForeignKey(
        User, on_delete=models.CASCADE,
        related_name='recipes'
    )

    title = models.CharField(max_length=200, validators=[validate_no_profanity])
    description = models.TextField(blank=True, null=True, validators=[validate_no_profanity])

    def clean(self):
        # Sanitize the description before saving.
        if self.description:
            allowed_tags = list(bleach.sanitizer.ALLOWED_PROTOCOLS)
            allowed_tags.extend(['p', 'strong', 'em'])
            allowed_attrs = {}
            self.description = bleach.clean(
                self.description, 
                tags=allowed_tags, 
                attributes=allowed_attrs,
            )
    
    def save(self, *args, **kwargs):
        self.full_clean
        super().save(*args, **kwargs)

    prep_time = models.IntegerField(
        validators=[MinValueValidator(0)],
        help_text="Cooking time in minutes"
    )
    cook_time = models.IntegerField(
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

    @property
    def total_time(self):
        return self.prep_time + self.cook_time
    
    class Meta:
        ordering = ['title']

    def __str__(self):
        return self.title