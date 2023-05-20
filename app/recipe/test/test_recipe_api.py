from django.contrib.auth import get_user_model
from django.urls import reverse
from django.test import TestCase

from rest_framework import status
from rest_framework.test import APIClient

from core.models import Recipe, Tag, Ingredient

from recipe.serializers import RecipeSerializer, RecipeDetailSerielizer

RECIPE_URL = reverse('recipe:recipe-list')

def detail_url(recipe_id):
    return reverse('recipe:recipe-detail', args=[recipe_id])

def sample_tag(user, name='choclet'):
    Tag.objects.create(user=user, name=name)

def sample_ingredient(user, name='test ingre'):
    Ingredient.objects.create(user=user, name=name)

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

    def test_recipe_view_details(self):
        "test reviewing recipe details"
        recipe = sample_recipe(user=self.user)
        recipe.tags.add(sample_tag(user=self.user))
        recipe.ingredients.add(sample_ingredient(user=self.user))
    
        url = detail_url(recipe.id)
        res = self.client.get(url)

        serializer = RecipeDetailSerielizer(recipe)
        self.assertEqual(res.data, serializer.data)


    def test_recipe_creating_success(self):
        """test create a recipe succesfulle"""
        payload = {
            'title': 'sample recipe',
            'time_minute':10,
            'price': 5.0
        }
        res = self.client.post(RECIPE_URL, payload)
        self.assertTupleEqual(res.status_code, status.HTTP_201_CREATED)

        exists = Recipe.objects.filter(title=payload['title']).exists()
        self.assertTrue(exists)

        recipes=Recipe.objects.get(id=res.data['id'])
        for key in payload.keys():
            self.assertEqual(payload[key], getattr(recipes, key))     
    

    def test_create_recipe_with_tags(self):
        """test creating a recipe with tag"""
        tag1 = sample_tag(user=self.user, name='Vegan')
        tag2 = sample_tag(user=self.user, name='Dessert')

        payload = {
            'title': 'Avacado Lim',
            'tags': [tag1.id, tag2.id],
            'time_minutes': 20.00,
            'price': 5.00
        }

        res = self.client.post(RECIPE_URL, payload)
        self.assertTupleEqual(res.status_code, status.HTTP_201_CREATED)

        recipe= Recipe.objects.get(id = res.data['id'])
        tags = recipe.tags.all()

        self.assertEqual(tags.count(), 2)
        self.assertIn(tag1, tags)
        self.assertIn(tag2, tags)

    def test_create_recipe_with_ingredients(self):
        """test creating a recipe with tag"""
        ingredient1 = sample_ingredient(user=self.user, name='Prown')
        ingredient2 = sample_ingredient(user=self.user, name='Ginger')

        payload = {
            'title': 'Avacado Lim',
            'tags': [ingredient1.id, ingredient2.id],
            'time_minutes': 10.00,
            'price': 5.00
        }

        res = self.client.post(RECIPE_URL, payload)
        self.assertTupleEqual(res.status_code, status.HTTP_201_CREATED)

        recipe= Recipe.objects.get(id = res.data['id'])
        ingredients = recipe.ingredients.all()

        self.assertEqual(ingredients.count(), 2)
        self.assertIn(ingredient1, ingredients)
        self.assertIn(ingredient2, ingredients)

    def test_partial_update_recipe(self):
        """test updating a recipe with patch """

        recipe = sample_recipe(user= self.user)
        recipe.tags.add(sample_tag(user=self.user))
        new_tags = sample_tag(user=self.user)
        pay_load = {
            'title':'chicken',
            'tags':[new_tags.id]
            }
        url = detail_url(recipe.id)
        self.client.patch(url, pay_load)

        recipe.refresh_from_db()

        self.assertEqual(recipe.title, pay_load['title'])
        tags = recipe.tags.all()
        self.assertEqual(len(tags), 1)
        self.assertIn(new_tags, tags)
        
    def test_full_update_recipe(self):
        """test updating recipe with put"""

        recipe=sample_recipe(user=self.user)
        recipe.tags.add(sample_tag(user=self.user))

        pay_load={
            'title':'spageti',
            'time_miinute':15,
            'price':5.00
        }
        url = detail_url(recipe.id)
        self.client.put(url,pay_load)

        recipe.refresh_from_db()
        self.assertEqual(recipe.title, pay_load['title'])
        self.assertEqual(recipe.title, pay_load['time_minute'])
        self.assertEqual(recipe.title, pay_load['price'])

        tags = recipe.tags.all()
        self.assertEqual(len(tags),0)
        
