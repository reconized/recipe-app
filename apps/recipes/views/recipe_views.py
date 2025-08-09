from rest_framework import generics
from rest_framework.permissions import IsAuthenticatedOrReadOnly
# from apps.recipes.permissions import IsOwnerOrReadOnly
from apps.recipes.models.recipe import Recipe
from apps.recipes.serializers.recipe_serializer import RecipeSerializer

class RecipeListCreate(generics.ListCreateAPIView):
    queryset = Recipe.objects.all()
    serializer_class = RecipeSerializer
    permission_classes = [IsAuthenticatedOrReadOnly]

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)

