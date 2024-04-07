from django.test import TestCase, RequestFactory
from django.contrib.auth.models import User
from django.contrib.messages.storage.fallback import FallbackStorage
from django.contrib import messages
from django.shortcuts import redirect

from mytownwebsite.views import signup

class SignupTestCase(TestCase):
    def setUp(self):
        self.factory = RequestFactory()

    def test_successful_signup(self):
        # Create a POST request with valid data
        request = self.factory.post('/signup/', {
            'username': 'testuser',
            'fname': 'Test',
            'lname': 'User',
            'email': 'test@example.com',
            'pass1': 'password123',
            'pass2': 'password123',
        })

        # Set up message storage
        setattr(request, '_messages', FallbackStorage(request))

        # Call the signup view function
        response = signup(request)

        # Verify that the user is redirected to the signin page
        self.assertEqual(response.url, '/signin/')

        # Verify that the user is created
        self.assertTrue(User.objects.filter(username='testuser').exists())

        # Verify success message is set
        messages.success.assert_called_once_with(request, "Your account has been successfully created!")

    def test_unsuccessful_signup_password_mismatch(self):
        # Create a POST request with mismatched passwords
        request = self.factory.post('/signup/', {
            'username': 'testuser',
            'fname': 'Test',
            'lname': 'User',
            'email': 'test@example.com',
            'pass1': 'password123',
            'pass2': 'password456',  # Mismatched password
        })

        # Set up message storage
        setattr(request, '_messages', FallbackStorage(request))

        # Call the signup view function
        response = signup(request)

        # Verify that the user is redirected back to the signup page
        self.assertEqual(response.url, '/signup/')

        # Verify that the user is not created
        self.assertFalse(User.objects.filter(username='testuser').exists())

        # Verify error message is set
        messages.error.assert_called_once_with(request, "Passwords do not match.")













