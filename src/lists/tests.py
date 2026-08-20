"""Testing lists app."""

from django.test import TestCase

from lists.models import Item


class HomePageTest(TestCase):
    """Tests for Home Page."""

    def test_uses_home_template(self) -> None:
        """Test return correct html for home page."""
        response = self.client.get("/")
        self.assertTemplateUsed(response, "home.html")

    def test_renders_input_form(self) -> None:
        """Test rendered input form of home page."""
        response = self.client.get("/")
        self.assertContains(response, '<form method="post" action="/">')
        self.assertContains(response, '<input name="item_text"')

    def test_can_save_a_post_request(self) -> None:
        """Test saving POST request."""
        self.client.post("/", data={"item_text": "A new list item"})
        self.assertEqual(Item.objects.count(), 1)
        new_item = Item.objects.first()
        assert new_item is not None
        self.assertEqual(new_item.text, "A new list item")

    def test_redirects_after_post(self) -> None:
        """Test redirect after POST request."""
        response = self.client.post("/", data={"item_text": "A new list item"})
        self.assertRedirects(response, "/lists/the-only-list-in-the-world/")

    def test_only_saves_items_when_necessary(self) -> None:
        """Test that Item does not save blank item."""
        self.client.get("/")
        self.assertEqual(Item.objects.count(), 0)

    '''
    def test_can_save_multiple_items(self) -> None:
        """Test saving multiple Items."""
        self.client.post("/", data={"item_text": "first item"})
        response = self.client.post("/", data={"item_text": "second item"})
        self.assertContains(response, "first item")
        self.assertContains(response, "second item")
    '''


class ItemModelTest(TestCase):
    """Test Item Model."""

    def test_saving_and_retrieving_items(self) -> None:
        """Test saving and retrieving items."""
        first_item = Item()
        first_item.text = "The first (ever) list item"
        first_item.save()

        second_item = Item()
        second_item.text = "Item the second"
        second_item.save()

        saved_items = Item.objects.all()
        self.assertEqual(saved_items.count(), 2)

        first_saved_item = saved_items[0]
        second_saved_item = saved_items[1]
        self.assertEqual(first_saved_item.text, "The first (ever) list item")
        self.assertEqual(second_saved_item.text, "Item the second")


class ListViewTest(TestCase):
    """Test LIst View."""

    def tests_uses_list_template(self) -> None:
        """Test that the correct template is used."""
        response = self.client.get("/lists/the-only-list-in-the-world/")
        self.assertTemplateUsed(response, "list.html")

    def test_renders_input_form(self) -> None:
        """Test rendered input form of home page."""
        response = self.client.get("/lists/the-only-list-in-the-world/")
        self.assertContains(response, '<form method="post" action="/">')
        self.assertContains(response, '<input name="item_text"')

    def test_displays_all_list_items(self) -> None:
        """Test display all list items on a get request."""
        Item.objects.create(text="itemy 1")
        Item.objects.create(text="itemy 2")

        response = self.client.get("/lists/the-only-list-in-the-world/")

        self.assertContains(response, "itemy 1")
        self.assertContains(response, "itemy 2")
