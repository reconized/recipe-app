from django.urls import path
from apps.recipes.views.locked_out_view import LockedOutView
from apps.recipes.views.login import LoginView
from apps.recipes.views.recipe_views import RecipeListCreate
from apps.recipes.views.recipe_detail_view import RecipeDetail

app_name = 'recipes'

urlpatterns = [
    # Categories endpoints
    # path('categories/', views.CategoriesView.as_view()),
    # path('categories/<int:pk>/', views.CategoryDetailView.as_view()),

    # User list endpoint
    # path('users/', views.UserList.as_view(), name='user-list'),

    # Recipes endpoints
    path('recipes/', RecipeListCreate.as_view(), name='recipe-list'),
    path('recipes/<int:pk>/', RecipeDetail.as_view(), name='recipe-detail'),

    # Manager group management endpoints
    # path('groups/manager/users/', views.ManagerGroupUserListCreateView.as_view()),
    # path('groups/manager/users/<int:pk>/', views.ManagerGroupUserDeleteView.as_view()),

    # Locked out view
    path('login/', LoginView.as_view(), name='login'),
    path('locked-out/', LockedOutView.as_view(), name='locked_out'),
]