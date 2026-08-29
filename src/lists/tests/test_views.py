"""Testing lists app."""

import lxml.html
from django.test import TestCase
from django.utils import html

from lists.models import Item, List


class HomePageTest(TestCase):
    """Tests for Home Page."""

    def test_uses_home_template(self) -> None:
        """Test return correct html for home page."""
        response = self.client.get("/")
        self.assertTemplateUsed(response, "home.html")

    def test_renders_input_form(self) -> None:
        """Test rendered input form of home page."""
        response = self.client.get("/")
        parsed = lxml.html.fromstring(response.content)
        [form] = parsed.cssselect("form[method=post]")
        self.assertEqual(form.get("action"), "/lists/new")
        text_inputs = form.cssselect("input")
        self.assertIn("item_text", [text_input.get("name") for text_input in text_inputs])

    '''
    def test_can_save_multiple_items(self) -> None:
        """Test saving multiple Items."""
        self.client.post("/", data={"item_text": "first item"})
        response = self.client.post("/", data={"item_text": "second item"})
        self.assertContains(response, "first item")
        self.assertContains(response, "second item")
    '''


class NewListTest(TestCase):
    """Test creating a new list."""

    def test_can_save_a_post_request(self) -> None:
        """Test saving POST request."""
        self.client.post("/lists/new", data={"item_text": "A new list item"})
        self.assertEqual(Item.objects.count(), 1)
        new_item = Item.objects.first()
        assert new_item is not None
        self.assertEqual(new_item.text, "A new list item")

    def test_redirects_after_post(self) -> None:
        """Test redirect after POST request."""
        response = self.client.post("/lists/new", data={"item_text": "A new list item"})
        new_list = List.objects.get()
        self.assertRedirects(response, f"/lists/{new_list.id}/")

    def test_validation_errors_are_sent_back_to_home_page_template(self) -> None:
        """Test validation errors are sent back to home page template."""
        response = self.client.post("/lists/new", data={"item_text": ""})
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, "home.html")
        expected_error = html.escape("You can't have an empty list item")
        self.assertContains(response, expected_error)

    def test_invalid_list_items_arent_saved(self) -> None:
        """Test invalid list items are not saved."""
        self.client.post("/lists/new", data={"item_text": ""})
        self.assertEqual(List.objects.count(), 0)
        self.assertEqual(Item.objects.count(), 0)


class NewItemTest(TestCase):
    """Test adding new item."""

    def test_can_save_a_post_request_to_an_existing_list(self) -> None:
        """Test post request to existing list."""
        other_list = List.objects.create()  # noqa: F841
        correct_list = List.objects.create()

        self.client.post(
            f"/lists/{correct_list.id}/add_item",
            data={"item_text": "A new item for an existing list"},
        )

        self.assertEqual(Item.objects.count(), 1)
        new_item = Item.objects.get()
        self.assertEqual(new_item.text, "A new item for an existing list")
        self.assertEqual(new_item.list, correct_list)

    def test_redirects_to_list_view(self) -> None:
        """Test redirect to list view."""
        other_list = List.objects.create()  # noqa: F841
        correct_list = List.objects.create()

        response = self.client.post(
            f"/lists/{correct_list.id}/add_item",
            data={"item_text": "A new item for an existing list"},
        )

        self.assertRedirects(response, f"/lists/{correct_list.id}/")


class ListViewTest(TestCase):
    """Test List View."""

    def tests_uses_list_template(self) -> None:
        """Test that the correct template is used."""
        mylist = List.objects.create()
        response = self.client.get(f"/lists/{mylist.id}/")
        self.assertTemplateUsed(response, "list.html")

    def test_renders_input_form(self) -> None:
        """Test rendered input form of home page."""
        mylist = List.objects.create()
        response = self.client.get(f"/lists/{mylist.id}/")
        parsed = lxml.html.fromstring(response.content)
        [form] = parsed.cssselect("form[method=post]")
        self.assertEqual(form.get("action"), f"/lists/{mylist.id}/add_item")
        text_inputs = form.cssselect("input")
        self.assertIn("item_text", [text_input.get("name") for text_input in text_inputs])

    def test_displays_only_items_for_that_list(self) -> None:
        """Test display all list items on a get request."""
        correct_list = List.objects.create()
        Item.objects.create(text="itemy 1", list=correct_list)
        Item.objects.create(text="itemy 2", list=correct_list)
        other_list = List.objects.create()
        Item.objects.create(text="other list item", list=other_list)

        response = self.client.get(f"/lists/{correct_list.id}/")

        self.assertContains(response, "itemy 1")
        self.assertContains(response, "itemy 2")
        self.assertNotContains(response, "other list item")
