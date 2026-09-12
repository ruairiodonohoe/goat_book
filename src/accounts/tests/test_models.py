"""Test models."""

from django.contrib import auth
from django.test import TestCase

from accounts.models import Token, User


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


class TokenModelTest(TestCase):
    """TokenModelTest Class."""

    def test_links_user_with_auto_generated_uid(self) -> None:
        """Test links user with auto generated uid."""
        token1 = Token.objects.create(email="a@b.com")
        token2 = Token.objects.create(email="a@b.com")
        self.assertNotEqual(token1.uid, token2.uid)
