from django.urls import path
from apps.recipe_api import views

urlpatterns = [
    # Categories endpoints
    # path('categories/', views.CategoriesView.as_view()),
    # path('categories/<int:pk>/', views.CategoryDetailView.as_view()),

    # Recipes endpoints
    # path('recipes/', views.RecipeListCreateView.as_view()),
    # path('recipes/<int:pk>/', views.RecipeDetailView.as_view()),

    # Manager group management endpoints
    # path('groups/manager/users/', views.ManagerGroupUserListCreateView.as_view()),
    # path('groups/manager/users/<int:pk>/', views.ManagerGroupUserDeleteView.as_view()),
]