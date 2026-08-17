"""Testing lists app."""

from django.test import TestCase


class HomePageTest(TestCase):
    """Tests for Home Page."""

    def test_uses_home_template(self) -> None:
        """Test return correct html for home page."""
        response = self.client.get("/")
        self.assertTemplateUsed(response, "home.html")

    def test_renders_homepage_content(self) -> None:
        """Test rendered content of home page."""
        response = self.client.get("/")
        self.assertContains(response, "To-Do")
