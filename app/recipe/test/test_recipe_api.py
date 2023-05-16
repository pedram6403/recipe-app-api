from django.contrib.auth import get_user_model
from django.urls import reverse
from django.test import TestCase

from rest_framework import status
from rest_framework.test import APIClient

from core.models import Recipe

from recipe.serializers import RecipeSerializer

RECIPE_URL = reverse('recipe:recipe-list')

def sample_recipe(user, **params):
    """create and retuen a sample recipe"""
    defaults = {
        'title': 'sample recipe',
        'time_minute':10,
        'price': 5.0
    }
    defaults.update(params)

    return Recipe.objects.create(user=user, **defaults)


class publicRecipeApiTest(TestCase):
    """test unauthenticated recipe API access"""
    def setUp(self):
        self.client=APIClient()
    
    def test_authentication_requeird(self):
        res = self.client.get(RECIPE_URL)

        self.assertEqual(res.status_code, status.HTTP_401_UNAUTHORIZED)


class privateRecipeApiTest(TestCase):
    """Test authenticated recipe API access """
    def setUp(self):
        self.client = APIClient()

        self.user = get_user_model().objects.create_user(
            'test@test.com',
            'testpass'
        )
        self.client.force_authenticate(self.user)

    def test_recip_retriving_ath_user(self):
        """Test if a authenticated user access to recipe"""
        sample_recipe(user=self.user)
        sample_recipe(user=self.user)

        res = self.client.get(RECIPE_URL)

        recipes = Recipe.objects.all().order_by('-id')
        serializer = RecipeSerializer(recipes, many=True)

        self.assertEqual(res.status_code, status.HTTP_200_OK)
        self.assertEqual(res.data, serializer.data)

    def test_recipe_limited_to_user(self):
        """Test the access of each user to recipe"""
        user2 = get_user_model().objects.create_user(
            'user2',
            'testpass'
        )
        sample_recipe(user=self.user)
        sample_recipe(user=user2)

        recipes = Recipe.objects.filter(user=self.user)
        serializer= RecipeSerializer(recipes, many=True)
        
        res= self.client.get(RECIPE_URL)

        self.assertEqual(len(res.data), 1)
        self.assertEqual(res.status_code, status.HTTP_200_OK)
        self.assertEqual(res.data, serializer.data)

    # def test_recipe_creating_success(self):
    #     """test create a recipe succesfulle"""
    #     payload = {
    #         'title': 'sample recipe',
    #         'time_minute':10,
    #         'price': 5.0
    #     }
    #     res = self.client.post(RECIPE_URL, payload)

    #     exists = Recipe.objects.filter(title=payload['title']).exists()
        

    #     self.assertTupleEqual(res.status_code, status.HTTP_201_CREATED)
    #     self.assertTrue(exists)
    
    # def test_recipe_invalid_name(self):
    #     payload ={
    #         'title':'',
    #         'time_minute':10,
    #         'price': 5.0
    #     }
    #     res = self.client.post(RECIPE_URL)
        
    #     self.assertEqual(res.status_code, status.HTTP_400_BAD_REQUEST)