from django.test import TestCase
from django.contrib.auth import get_user_model

class ModelTests(TestCase):
    '''test user models'''

    def test_create_user_with_email_successful(self):
        '''test user creation with email '''
        email = 'test@example.com'
        password = 'test@123'
        user = get_user_model().objects.create_user(
            email=email,
            password=password
        )

        self.assertEqual(user.email, email)
        self.assertTrue(user.check_password(password))

    def test_new_user_email_normalized(self):
        '''test email is normalized for new users'''
        sample_emails = [
            ('test1@EXAMPLE.COM', 'test1@example.com'),
            ('Test2@EXAMPLE.COM', 'Test2@example.com'),
            ('test3@example.com', 'test3@example.com'),
            ('TEST4@EXAMPLE.COM', 'TEST4@example.com'),
        ]
        for email, expected in sample_emails:
            user = get_user_model().objects.create_user(email, 'sample123')
            self.assertEqual(user.email, expected)

    def test_new_user_without_email_raises_error(self):
        '''new user without user email raises email error'''
        with self.assertRaises(ValueError):
            get_user_model().objects.create_user('', 'test123')

    def test_create_super_user(self):
        '''test creating super user'''
        user = get_user_model().objects.create_superuser(
            email='test.example.com',
            password='test@123'
        )
        self.assertTrue(user.is_superuser)
        self.assertTrue(user.is_staff)