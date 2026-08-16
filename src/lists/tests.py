"""Testing lists app."""

from django.test import TestCase


class SmokeTest(TestCase):
    """Smoke test."""

    def test_bad_maths(self) -> None:
        """Test fail."""
        self.assertEqual(1 + 1, 3)
