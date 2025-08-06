from apps.recipes.tests.test_setup import RecipeTestSetup
from rest_framework import status

class AuthPermissionTests(RecipeTestSetup):
    def test_unauthenticated_user_can_list_recipes(self):
        self.client.logout()
        response = self.client.get(self.recipe_list_url)
        print(f'Response data length in test: {len(response.data)}')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        print(f'Full response data: {response.data}')
        self.assertEqual(len(response.data['results']), 1)