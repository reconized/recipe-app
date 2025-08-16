from apps.recipes.tests.test_setup import RecipeTestSetup
from apps.recipes.models.recipe import Recipe
from rest_framework import status

class AuthPermissionTests(RecipeTestSetup):
    def test_unauthenticated_user_can_list_recipes(self):
        self.client.logout()
        response = self.client.get(self.recipe_list_url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data['results']), 1)

    def test_unauthenticated_user_can_retrieve_recipe(self):
        self.client.logout()
        response = self.client.get(self.recipe_detail_url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['title'], self.recipe.title)

    def test_unauthenticated_user_cannot_create_recipe(self):
        self.client.logout()
        data = {
            'user_id': self.user.id,
            'title': 'New Recipe',
            'description': 'A new recipe.',
            'prep_time': 10,
            'cook_time': 20,
            'servings': 2,
            'category': self.category.id
        }

        response = self.client.post(self.recipe_list_url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_user_cannot_update_another_users_recipe(self):
        self.client.force_authenticate(user=self.user2)
        data = {'title': 'Updated Title by Owner'}
        response = self.client.patch(self.recipe_detail_url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_user_can_update_their_own_recipe(self):
        self.client.force_authenticate(user=self.user)
        data = {'title': 'Updated Title by Owner'}
        response = self.client.patch(self.recipe_detail_url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(Recipe.objects.get(id=self.recipe.id).title, 'Updated Title by Owner')

    def test_user_can_delete_their_own_recipe(self):
        self.client.force_authenticate(user=self.user)
        response = self.client.delete(self.recipe_detail_url)
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        self.assertEqual(Recipe.objects.count(), 0)

    def test_user_cannot_delete_another_users_recipe(self):
        self.client.force_authenticate(user=self.user2)
        response = self.client.delete(self.recipe_detail_url)
        self.assertEqual(Recipe.objects.count(), 1)

class RecipeModelTests(RecipeTestSetup):
    def test_recipe_model_creation(self):
        recipe = Recipe.objects.get(id=self.recipe.id)
        self.assertEqual(recipe.title, 'Test Recipe')
        self.assertEqual(recipe.user, self.user)
        self.assertEqual(recipe.prep_time, 15)
        self.assertEqual(recipe.cook_time, 30)
        self.assertEqual(recipe.servings, 4)

    def test_ingredient_and_instructions_are_nested_in_recipe_response(self):
        self.client.force_authenticate(user=self.user)
        response = self.client.get(self.recipe_detail_url)

        self.assertEqual(response.status_code, status.HTTP_200_OK)

        self.assertIn('ingredients', response.data)
        self.assertEqual(len(response.data['ingredients']), 1)
        self.assertEqual(response.data['ingredients'][0]['name'], 'Test Ingredient')

        self.assertIn('instructions', response.data)
        self.assertEqual(len(response.data['instructions']), 1)
        self.assertEqual(response.data['instructions'][0]['step_number'], 1)
        self.assertEqual(response.data['instructions'][0]['description'], 'Test Instruction.')

    def test_validation_for_invalid_data(self):
        self.client.force_authenticate(user=self.user)
        invalid_data = {
            'title': 'Invalid Recipe',
            'prep_time': -10,
            'cook_time': 20,
            'servings': 2,
            'category': self.category.id
        }
        response = self.client.post(self.recipe_list_url, invalid_data, format='json')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertIn('prep_time', response.data)

        invalid_data_2 = {
            'prep_time': 10,
            'cook_time': 20,
            'servings': 2,
            'category': self.category.id
        }

        response_2 = self.client.post(self.recipe_list_url, invalid_data_2, format='json')
        self.assertEqual(response_2.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertIn('title', response_2.data)

    def test_profanity_check_validator(self):
        self.client.force_authenticate(user=self.user)

        profane_data = {
            'title': 'This is a fucking great recipe',
            'description': 'A test description.',
            'prep_time': 10,
            'cook_time': 20,
            'servings': 2,
            'category': self.category.id
        }

        response = self.client.post(self.recipe_list_url, profane_data, format='json')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertIn('This content contains inappropriate language and is not allowed.', response.data['title'][0])