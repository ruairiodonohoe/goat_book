"""Testing lists app."""

from django.test import TestCase


class HomePageTest(TestCase):
    """Tests for Home Page."""

    def test_uses_home_template(self) -> None:
        """Test return correct html for home page."""
        response = self.client.get("/")
        self.assertTemplateUsed(response, "home.html")

    def test_renders_input_form(self) -> None:
        """Test rendered input form of home page."""
        response = self.client.get("/")
        self.assertContains(response, '<form method="post">')
        self.assertContains(response, '<input name="item_text"')

    def test_can_save_a_post_request(self) -> None:
        """Test saving POST request."""
        response = self.client.post("/", data={"item_text": "A new list item"})
        self.assertContains(response, "A new list item")
        self.assertTemplateUsed(response, "home.html")
