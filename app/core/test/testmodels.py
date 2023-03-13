from django.test import TestCase
from django.contrib.auth import get_user_model

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
        
