from django.test import TestCase
from django.contrib.auth import get_user_model
from django.urls import reverse

from rest_framework.test import APIClient
from rest_framework import status

CREATE_USER_URL = reverse('user:create')
TOKEN_URL = reverse('user:token_obtain_pair')

def create_user(**kwargs):
    '''create and return a new user'''
    return get_user_model().objects.create_user(
        **kwargs
    )

class PublicUserAPITest(TestCase):
    '''test the public user apis'''

    def setUP(self):
        self.client = APIClient()

    def test_create_user_success(self):
        '''test creating a user is successful'''

        payload = dict(
            email='test@example.com',
            password='Dock@123',
            name='testuser'
        )
        res = self.client.post(CREATE_USER_URL, payload)

        self.assertEqual(res.status_code, status.HTTP_201_CREATED)

        user = get_user_model().objects.get(email=payload['email'])
        self.assertTrue(user.check_password(payload['password']))
        self.assertNotIn('password', res.data)

    def test_user_with_email_exists_error(self):
        '''test error returned if user with email exisits'''
        payload = dict(
            email='test@example.com',
            password='testpass123',
            name='testuser'
        )
        create_user(**payload)
        res = self.client.post(CREATE_USER_URL, payload)

        self.assertEqual(res.status_code, status.HTTP_400_BAD_REQUEST)

    def test_password_too_short_error(self):
        '''test error is returned if password less than 5 chars'''
        payload = dict(
            email='test@example.com',
            password='te',
            name='testuser'
        )
        self.client.post(CREATE_USER_URL, payload)
        user_exists = get_user_model().objects.filter(
            email=payload['email']
        ).exists()

        self.assertFalse(user_exists)

    def test_create_token_for_user(self):
        '''test create jet token for user'''
        user_credentials = {
            'name':'Test User',
            'email':'test@example.com',
            'password':'test@123'
        }

        create_user(**user_credentials)

        payload = {
            'email':'test@example.com',
            'password':'test@123'
        }

        res = self.client.post(TOKEN_URL, payload)

        self.assertIn('access', res.data)
        self.assertIn('refresh', res.data)
        self.assertEqual(res.status_code, status.HTTP_200_OK)

    def test_create_token_bad_creds(self):
        '''test returns error if credentials invalid'''
        user_credentials = {
            'name':'Test User',
            'email':'test@example.com',
            'password':'test@123'
        }
        create_user(**user_credentials)
        payload = {
            'email':'test@example.com',
            'password':'wrong'
        }

        res = self.client.post(TOKEN_URL, payload)

        self.assertNotIn('access', res.data)
        self.assertNotIn('refresh', res.data)
        self.assertEqual(res.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_create_token_blank_password(self):
        '''test create user with blank password'''
        payload = {
            'email':'test@example.com',
            'name':'test',
            'password':''
        }

        res = self.client.post(CREATE_USER_URL, payload)

        self.assertNotIn('access', res.data)
        self.assertNotIn('refresh', res.data)
        self.assertEqual(res.status_code, status.HTTP_400_BAD_REQUEST)

    def test_create_invalid_password_string(self):
        '''test create user with an invalid string'''
        payload = {
            'email':'test@example.com',
            'name':'test',
            'password':'~~~ ~~'
        }

        res = self.client.post(CREATE_USER_URL, payload)

        self.assertNotIn('access', res.data)
        self.assertNotIn('refresh', res.data)
        self.assertEqual(res.status_code, status.HTTP_400_BAD_REQUEST)

    def test_create_password_no_uppercase(self):
        '''Test creating user with a password lacking an uppercase letter'''
        payload = {
            'email': 'nousercase@example.com',
            'name': 'nousercase',
            'password': 'invalid@123'
        }

        res = self.client.post(CREATE_USER_URL, payload)

        self.assertNotIn('access', res.data)
        self.assertNotIn('refresh', res.data)
        self.assertEqual(res.status_code, status.HTTP_400_BAD_REQUEST)

    def test_create_password_no_lowercase(self):
        '''Test creating user with a password lacking a lowercase letter'''
        payload = {
            'email': 'nolowercase@example.com',
            'name': 'nolowercase',
            'password': 'INVALID@123'
        }

        res = self.client.post(CREATE_USER_URL, payload)

        self.assertNotIn('access', res.data)
        self.assertNotIn('refresh', res.data)
        self.assertEqual(res.status_code, status.HTTP_400_BAD_REQUEST)

    def test_create_password_no_digit(self):
        '''Test creating user with a password lacking a digit'''
        payload = {
            'email': 'nodigit@example.com',
            'name': 'nodigit',
            'password': 'Invalid@Password'
        }

        res = self.client.post(CREATE_USER_URL, payload)

        self.assertNotIn('access', res.data)
        self.assertNotIn('refresh', res.data)
        self.assertEqual(res.status_code, status.HTTP_400_BAD_REQUEST)

    def test_create_password_no_special_char(self):
        '''Test creating user with a password lacking a special character'''
        payload = {
            'email': 'nospecialchar@example.com',
            'name': 'nospecialchar',
            'password': 'Invalid123'
        }

        res = self.client.post(CREATE_USER_URL, payload)

        self.assertNotIn('access', res.data)
        self.assertNotIn('refresh', res.data)
        self.assertEqual(res.status_code, status.HTTP_400_BAD_REQUEST)

    def test_create_password_similar_to_username(self):
        '''Test creating user with a password similar to username'''
        payload = {
            'email': 'test@example.com',
            'name': 'testuser',
            'password': 'tszx@u@ser'
        }

        res = self.client.post(CREATE_USER_URL, payload)

        self.assertNotIn('access', res.data)
        self.assertNotIn('refresh', res.data)
        self.assertEqual(res.status_code, status.HTTP_400_BAD_REQUEST)

    def test_create_password_similar_to_email(self):
        '''Test creating user with a password similar to email'''
        payload = {
            'email': 'test@example.com',
            'name': 'testuser',
            'password': 'tszx@u@.co'
        }

        res = self.client.post(CREATE_USER_URL, payload)

        self.assertNotIn('access', res.data)
        self.assertNotIn('refresh', res.data)
        self.assertEqual(res.status_code, status.HTTP_400_BAD_REQUEST)