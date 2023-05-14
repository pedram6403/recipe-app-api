from django.test import TestCase
from django.contrib.auth import get_user_model
from core import models


def sample_user(email='test@email.com', password='testpassword'):
    "create simple user for test"
    return get_user_model().objects.create_user(email, password)


class ModelTest(TestCase):
    def test_create_user_with_email_successful(self):
        email = "test@mail.com"
        password = "Test1234567"
        user = get_user_model().objects.create_user(
            email=email,
            password=password,
        )

        self.assertEqual(user.email, email)
        self.assertTrue(user.check_password(password))

    def test_new_user_normalize_email(self):
        """New user email normalize test"""
        email = "test@SDD.ASDFDS"
        password = 'test123'
        user = get_user_model().objects.create_user(email=email,password=password)

        self.assertEqual(user.email, email.lower())
    
    def test_new_user_invalid_email(self):
        with self.assertRaises(ValueError):
            get_user_model().objects.create_user(None, 'test123')

    def test_create_new_superuser(self):
        user = get_user_model().objects.create_superuser('test@test.dom', 'test12345')
        self.assertTrue(user.is_staff)
        self.assertTrue(user.is_superuser)
        
    def test_tag_str(self):
        """test the tag string represantation"""
        tag = models.Tag.objects.create(user=sample_user(), name='vegan')
        self.assertEqual(str(tag), tag.name)

    def test_ingredient_str(self):
        """test the ingredient string representation"""
        ingredient = models.Ingredient.objects.create(user=sample_user(), name='Cucumber')
        self.assertEqual(str(ingredient),ingredient.name)