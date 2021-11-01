"""Test for polls authentication."""
from django.contrib.auth.models import User
from django.test import TestCase
from django.shortcuts import reverse


class AuthenticationTest(TestCase):
    """Test cases for authentication system."""

    def setUp(self):
        """Initialize the user."""
        self.user = {
            'username': 'Noobmaster69',
            'password': '12345Iheretoo'
        }
        User.objects.create_user(**self.user)

    def test_logged_in_for_user(self):
        """Test user logged in, the user username should display on the index page."""
        response = self.client.post(reverse('login'), self.user)
        self.assertEqual(response.status_code, 302)
        response = self.client.get(reverse('polls:index'))
        self.assertTrue(response.context['user'].is_authenticated)

    def test_logged_out_for_user(self):
        """Test logged out, the user username will be not shown on the index page."""
        self.client.post(reverse('login'), self.user)
        response = self.client.post(reverse('logout'))
        self.assertEqual(response.status_code, 200)
        self.assertFalse(response.context['user'].is_authenticated)
