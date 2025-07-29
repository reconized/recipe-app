from django.contrib import admin
from apps.recipe_api.models import (
    Category, Recipe, Ingredient, Instruction
)

# Register your models here.
admin.site.register(Category)
admin.site.register(Recipe)
admin.site.register(Ingredient)
admin.site.register(Instruction)
