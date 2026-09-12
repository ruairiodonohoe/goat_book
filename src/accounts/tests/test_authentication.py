"""Test account authentication."""

from django.http import HttpRequest
from django.test import TestCase

from accounts.authentication import PasswordlessAuthenticationBackend
from accounts.models import Token, User


class AuthenticateTest(TestCase):
    """AuthenticateTest Class."""

    def test_returns_none_if_no_such_token(self) -> None:
        """Test returns None if no such token."""
        result = PasswordlessAuthenticationBackend().authenticate(HttpRequest(), "no-such-token")
        self.assertIsNone(result)

    def test_returns_new_user_with_correct_email_if_token_exists(self) -> None:
        """Test returns new  user with correct email if token exists."""
        email = "edith@example.com"
        token = Token.objects.create(email=email)
        user = PasswordlessAuthenticationBackend().authenticate(HttpRequest(), token.uid)
        new_user = User.objects.get(email=email)
        self.assertEqual(user, new_user)

    def test_returns_existing_user_with_correct_email_if_token_exists(self) -> None:
        """Test returns existing user with correct email if token exists."""
        email = "edith@example.com"
        existing_user = User.objects.create(email=email)
        token = Token.objects.create(email=email)
        user = PasswordlessAuthenticationBackend().authenticate(HttpRequest(), token.uid)
        self.assertEqual(user, existing_user)


class GetUserTest(TestCase):
    """GetUserTest class."""

    def test_gets_user_by_email(self) -> None:
        """Test gets user by email."""
        User.objects.create(email="another@example.com")
        desired_user = User.objects.create(email="edith@example.com")
        found_user = PasswordlessAuthenticationBackend().get_user("edith@example.com")
        self.assertEqual(found_user, desired_user)

    def test_returns_none_if_no_user_with_that_email(self) -> None:
        """Test return None if no user with that email."""
        self.assertIsNone(PasswordlessAuthenticationBackend().get_user("edith@example.com"))
