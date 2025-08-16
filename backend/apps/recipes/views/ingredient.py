from django.db import transaction
from rest_framework import viewsets
from rest_framework.exceptions import PermissionDenied
from apps.recipes.models.ingredient import Ingredient
from apps.recipes.models.recipe import Recipe
from apps.recipes.serializers.ingredient import IngredientSerializer
from apps.recipes.permissions import IsRecipeOwnerForChildren

class IngredientViewSet(viewsets.ModelViewSet):
    serializer_class = IngredientSerializer
    permission_classes = [IsRecipeOwnerForChildren]

    def get_queryset(self):
        qs = Ingredient.objects.select_related("recipe").all()
        recipe_pk = self.kwargs.get("recipe_pk")
        if recipe_pk:
            qs = qs.filter(recipe_id=recipe_pk)
        return qs
    
    def _assert_owner(self, recipe: Recipe):
        if self.request.user.is_staff:
            return
        if recipe.user_id != self.request.user.id:
            raise PermissionDenied("Only recipe owners can modify ingredients.")
    
    @transaction.atomic
    def perform_create(self, serializer):
        recipe_pk = self.kwargs.get("recipe_pk")
        if recipe_pk:
            recipe = Recipe.objects.get(pk=recipe_pk)
            self._assert_owner(recipe)
            serializer.save(recipe=recipe)
        else:
            recipe = serializer.validated_data.get("recipe")
            self._assert_owner(recipe)
            serializer.save(recipe=recipe)

    @transaction.atomic
    def perform_update(self, serializer):
        instance = self.get_object()
        self._assert_owner(instance.recipe)
        serializer.save()
    
    @transaction.atomic
    def perform_destroy(self, instance):
        self._assert_owner(instance.recipe)
        instance.delete()
