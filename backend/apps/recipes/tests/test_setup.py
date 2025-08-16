from django.urls import reverse
from django.contrib.auth.models import User
from rest_framework import status
from rest_framework.test import APITestCase
from apps.recipes.models.recipe import Recipe
from apps.recipes.models.ingredient import Ingredient
from apps.recipes.models.instruction import Instruction
from apps.recipes.models.category import Category

class RecipeTestSetup(APITestCase):
    def setUp(self):
        self.user = User.objects.create_user(
            username='testuser',
            password='password123'
        )
        self.user2 = User.objects.create_user(
            username='user2',
            password='password123'
        )
        self.category = Category.objects.create(
            name='Test Category'
        )
        self.recipe = Recipe.objects.create(
            title='Test Recipe',
            description='A simple test recipe.',
            prep_time=15,
            cook_time=30,
            servings=4,
            category=self.category,
            user=self.user
        )

        Ingredient.objects.create(
            recipe=self.recipe,
            name='Test Ingredient',
            quantity=1,
            unit='cup'
        )
        Instruction.objects.create(
            recipe=self.recipe,
            step_number=1,
            description='Test Instruction.'
        )

        # URLs
        self.recipe_list_url = reverse('recipes:recipe-list')
        self.recipe_detail_url = reverse('recipes:recipe-detail', args=[self.recipe.id])
