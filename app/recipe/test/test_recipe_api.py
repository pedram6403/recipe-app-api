from django.contrib.auth import get_user_model
from django.urls import reverse
from django.test import TestCase

from rest_framework import status
from rest_framework.test import APIClient

from core.models import Recipe

from recipe.serializers import RecipeSerializer

RECIPE_URL = reverse('recipe:recipe_list')

def sample_recipe(user, **params):
    """create and retuen a sample recipe"""
    defaults = {
        'title': 'sample recipe',
        'time_minute':10,
        'price': 5.0
    }
    defaults.update(params)

    return Recipe.objects.create(user=user, **defaults)