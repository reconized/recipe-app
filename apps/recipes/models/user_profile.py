from django.db import models
from django.contrib.auth.models import User
from apps.recipes.validators import validate_no_profanity

class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    display_name = models.CharField(
        max_length=50,
        blank=True,
        validators=[validate_no_profanity],
        help_text='A public name for your profile.'
    )

    def __str__(self):
        return f'{self.user.username} Profile'