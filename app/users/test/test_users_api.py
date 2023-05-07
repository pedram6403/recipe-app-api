from django.test import TestCase
from django.contrib.auth  import get_user_model
from django.urls import reverse

from rest_framework.test import APIClient
from rest_framework import status

CREATE_USER_URL = reverse('users:create')
TOKEN_URL = reverse('users:token')

def create_user(**params):
    return get_user_model().objects.create_user(**params)

class PublicUserApiTests(TestCase):
    """Test the user Api public"""
    def setUp(self):
        self.client =APIClient()

    def test_create_valid_user_success(self):
        """test creating user with valid payload is success"""
        payload = {
            'email':'test@test.com',
            'password':'testpass@123',
            'name':'testname',
        }
        res = self.client.post(CREATE_USER_URL, payload)
        self.assertEqual(res.status_code,status.HTTP_201_CREATED)
        user = get_user_model().objects.get(**res.data)
        # self.assertTrue(user.check_password(payload['password']))
        self.assertNotIn('password', res.data)
    
    def create_test_user_exists(self):
        """Test creating user that already exists"""
        payload = {'email':'test@mail.com', 'password': 'testpassword'}
        create_user(**payload)
        res = self.client.post(CREATE_USER_URL, payload)
        self.assertEqual(res.status_code, status.HTTP_400_BAD_REQUEST)
    
    def test_password_too_short(self):
        """test check the short password"""
        payload = {'email':'test@mail.com', 'password': 'pa'}
        res = self.client.post(CREATE_USER_URL, payload)
        self.assertEqual(res.status_code, status.HTTP_400_BAD_REQUEST)
        user_exists = get_user_model().objects.filter(email = payload['email']).exists()
        self.assertFalse(user_exists)
    
    def test_create_token_for_user(self):
        """test create a token for user"""
        payload = {'email':'test@test.com', 'password':'testpassword'}

        create_user(**payload)
        res = self.client.post(TOKEN_URL, payload)
        self.assertIn('token',res.data)
        self.assertEqual(res.status_code, status.HTTP_200_OK)

    def test_create_token_invalid_credantioal(self):
        create_user(email='test@test.com', password='testpassword')
        payload = {'email':'test@test.com', 'password':'wrongpass'}

        res = self.client.post(TOKEN_URL, payload)
        self.assertNotIn('token', res.data)
        self.assertEqual(res.status_code, status.HTTP_400_BAD_REQUEST)

    def test_create_token_no_user(self):
        """test create token if user not exist"""
        payload = {'email':'test@test.com', 'password':'testpassword'}

        res = self.client.post(TOKEN_URL, payload)
        self.assertNotIn('token', res.data)
        self.assertEqual(res.status_code, status.HTTP_400_BAD_REQUEST)

    def test_create_token_missing_fields(self):
        """test create token ifa field is empty"""
        payload = {'email':'test@test.com', 'password':''}

        res = self.client.post(TOKEN_URL, payload)
        self.assertNotIn('token', res.data)
        self.assertEqual(res.status_code, status.HTTP_400_BAD_REQUEST)