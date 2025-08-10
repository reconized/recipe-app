from rest_framework import generics
from rest_framework import permissions
from apps.recipes.models.ingredient import Ingredient
from apps.recipes.serializers.ingredient_serializer import IngredientSerializer

class IngredientDetail(generics.RetrieveUpdateDestroyAPIView):
    queryset = Ingredient.objects.all()
    serializer_class = IngredientSerializer
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]