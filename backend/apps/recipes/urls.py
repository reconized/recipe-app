from django.urls import path, include
from rest_framework.routers import DefaultRouter
from rest_framework_nested.routers import NestedDefaultRouter
from apps.recipes.views.recipe import RecipeViewSet
from apps.recipes.views.taxonomy import CuisineViewSet, CategoryViewSet
from apps.recipes.views.ingredient import IngredientViewSet
from apps.recipes.views.instruction import InstructionViewSet
from apps.recipes.views.profile import ProfileViewSet

app_name = 'recipes'

# Base router
router = DefaultRouter()
router.register(r"recipes", RecipeViewSet, basename="recipe")
router.register(r"cuisines", CuisineViewSet, basename="cuisine")
router.register(r"categories", CategoryViewSet, basename="category")
router.register(r"profiles", ProfileViewSet, basename="profile")

cuisine_router = NestedDefaultRouter(router, r"cuisines", lookup="cuisine")
cuisine_router.register(r"recipes", RecipeViewSet, basename="cuisine-recipes")

category_router = NestedDefaultRouter(router, r"categories", lookup="category")
category_router.register(r"recipes", RecipeViewSet, basename="category-recipes")

# # Nested under recipes: /api/recipes/{id}/ingredients|instructions/
recipe_router = NestedDefaultRouter(router, r"recipes", lookup="recipe")
recipe_router.register(r"ingredients", IngredientViewSet, basename="recipe-ingredients")
recipe_router.register(r"instructions", InstructionViewSet, basename="recipe-instructions")

urlpatterns = [
    path('', include(router.urls)),
    path('', include(recipe_router.urls)),
]