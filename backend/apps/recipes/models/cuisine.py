from django.db import models

class Cuisine(models.Model):
    name = models.CharField(max_length=100, unique=True)

    parent = models.ForeignKey(
        'self',
        on_delete=models.CASCADE,
        null=True,
        blank=True,
        related_name='subcategories'
    )

    class Meta:
        ordering = ['name']

    def __str__(self):
        return f"{self.name} (Subcategory of {self.parent})" if self.parent else self.name
    