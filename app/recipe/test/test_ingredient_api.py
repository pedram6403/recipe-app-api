from django.contrib.auth import get_user_model
from django.urls import reverse
from django.test import TestCase

from rest_framework import status
from rest_framework.test import APIClient

from core.models import Ingredient, Recipe

from recipe.serializers import IngredientSerializer

INGREDIENT_URL = reverse('recipe:ingredient-list')
class PublicIngredientApiTest(TestCase):
    """Test Ingredient publicity available"""
    def setUp(self):
        self.client = APIClient()

    def test_login_requered(self):
        """login is requered for access to ingredient"""
        res = self.client.get(INGREDIENT_URL)
        self.assertEqual(res.status_code, status.HTTP_401_UNAUTHORIZED)


class PrivateIngredientApiTest(TestCase):
    """Test Ingredient for authenticated users"""
    def setUp(self):
        self.client = APIClient()
        self.user = get_user_model().objects.create_user(
            email='test@test.com',
            password='testpassword'
        )
        self.client.force_authenticate(self.user)

    def test_retrive_Ingredient(self):
        """test retriving tags"""
        Ingredient.objects.create(user=self.user, name='cucomber')
        Ingredient.objects.create(user=self.user, name='udhh')

        res = self.client.get(INGREDIENT_URL)

        ingredients = Ingredient.objects.all().order_by('-name')
        serializer = IngredientSerializer(ingredients, many=True)

        self.assertEqual(res.status_code, status.HTTP_200_OK)
        self.assertEqual(res.data, serializer.data)

    def test_ingredient_limited_to_user(self):
        """test each user can see his own ingredient"""
        user2 = get_user_model().objects.create_user('test2@test.com', 'testpassword')
        Ingredient.objects.create(user=user2, name='cuc')
        ingredient = Ingredient.objects.create(user=self.user, name='uqo')

        res = self.client.get(INGREDIENT_URL)

        self.assertEqual(len(res.data),1)
        self.assertEqual(res.data[0]['name'], ingredient.name)
        self.assertEqual(res.status_code, status.HTTP_200_OK)

    def test_create_ingredient_successfuly(self):
        """test create a new ingredient successfuly"""
        payload = {
            'name':'cucomber'
        }
        res= self.client.post(INGREDIENT_URL, payload)
        exists = Ingredient.objects.filter(user=self.user, name=payload['name']).exists()

        self.assertEqual(res.status_code, status.HTTP_201_CREATED)
        self.assertTrue(exists)
        
    def test_ingredient_invalid_name(self):
        """test creating ingredient with invalid name"""
        payload = {
            'name':''
        }
        res= self.client.post(INGREDIENT_URL, payload)

        self.assertEqual(res.status_code, status.HTTP_400_BAD_REQUEST)

    def test_retrivins_ingredients_assigned_to_recipe(self):
        """test filtering the ingredients those assigned to a recipe"""

        ingredient1 = Ingredient.objects.create(user=self.user, name='ing1')
        ingredient2 = Ingredient.objects.create(user=self.user, name='ing2')

        recipe= Recipe.objects.create(
            user=self.user,
            title='food1',
            time_minute=5,
            price=5.0
        )

        recipe.ingredients.add(ingredient1)

        res = self.client.get(INGREDIENT_URL, {'assigned_only':1})
        
        serializer1 = IngredientSerializer(ingredient1)
        serializer2 = IngredientSerializer(ingredient2)

        self.assertIn(serializer1.data, res.data)
        self.assertNotIn(serializer2.data, res.data)
