"""Testing lists app."""

from django.test import TestCase


class HomePageTest(TestCase):
    """Tests for Home Page."""

    def test_home_page_returns_correct_html(self) -> None:
        """Test return correct html for home page."""
        response = self.client.get("/")
        self.assertContains(response, "<title>To-Do lists</title>")
        self.assertContains(response, "<html>")
        self.assertContains(response, "</html>")
