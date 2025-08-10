from django.shortcuts import render, get_object_or_404
from apps.recipes.models.recipe import Recipe
from apps.recipes.models.instruction import Instruction

def recipe_detail(request, recipe_id):
    recipe = get_object_or_404(Recipe, pk=recipe_id)
    instructions = recipe.instructions.all()
    ingredients = recipe.ingredients.all()

    context = {
        'recipe': recipe,
        'instructions': instructions,
        'ingredients': ingredients,
    }
    return render(request, 'recipe_detail.html', context)