"""Test models."""

from django.contrib import auth
from django.test import TestCase

from accounts.models import User


class UserModelTest(TestCase):
    """UserModelTest class."""

    def test_model_is_configured_for_django_auth(self) -> None:
        """Test model is configures for django auth."""
        self.assertEqual(auth.get_user_model(), User)

    def test_user_is_valid_with_email_only(self) -> None:
        """Test user is valid with email only."""
        user = User(email="a@b.com")
        user.full_clean()  # should not raise

    def test_email_is_primary_key(self) -> None:
        """Test email is primary key."""
        user = User(email="a@b.com")
        self.assertEqual(user.pk, "a@b.com")
