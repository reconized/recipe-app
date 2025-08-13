from django.urls import path
from apps.recipes.views.locked_out_view import LockedOutView
from apps.recipes.views.login import LoginView
from apps.recipes.views.recipe_view import RecipeListCreate
from apps.recipes.views.recipe_detail_view import RecipeDetail
from apps.recipes.views.category_list_view import CategoryListCreate
from apps.recipes.views.category_detail_view import CategoryDetail
from apps.recipes.views.ingredient_list_view import IngredientListCreate
from apps.recipes.views.ingredient_detail_view import IngredientDetail
from apps.recipes.views.instruction_list_view import InstructionListCreate
from apps.recipes.views.instruction_detail_view import InstructionDetail
from apps.recipes.views.recipe import recipe_detail

app_name = 'recipes'

urlpatterns = [
    # Categories endpoints
    path('categories/', CategoryListCreate.as_view()),
    path('categories/<int:pk>/', CategoryDetail.as_view()),

    # Recipes endpoints
    path('recipe-detail/<int:recipe_id>/', recipe_detail, name='standalone_view'),
    path('recipes/', RecipeListCreate.as_view(), name='recipe-list'),
    path('recipes/<int:pk>/', RecipeDetail.as_view(), name='recipe-detail'),

    # Ingredients endpoints
    path('ingredients/', IngredientListCreate.as_view(), name='ingredient-list'),
    path('ingredients/<int:pk>/', IngredientDetail.as_view(), name='ingredient-detail'),

    # Instruction endpoints
    path('instructions/', InstructionListCreate.as_view(), name='instruction-list'),
    path('instructions/<int:pk>/', InstructionDetail.as_view(), name='instruction-detail'),


    # Locked out view
    path('locked-out/', LockedOutView.as_view(), name='locked_out'),
]