from rest_framework import generics
from apps.recipes.models.recipe import Recipe
from apps.recipes.serializers.recipe_serializer import RecipeSerializer

class RecipeListCreate(generics.ListCreateAPIView):
    queryset = Recipe.objects.all()
    serializer_class = RecipeSerializer
