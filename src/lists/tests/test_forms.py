"""Tests for Forms."""

from django.test import TestCase

from lists.forms import EMPTY_ITEM_ERROR, ItemForm
from lists.models import Item, List


class ItemFormTest(TestCase):
    """Tests Item Form."""

    def test_form_item_input_has_placeholder_and_css_classes(self) -> None:
        """Test form item input has placeholder and css classes."""
        form = ItemForm()
        rendered = form.as_p()
        self.assertIn('placeholder="Enter a to-do item"', rendered)
        self.assertIn('class="form-control form-control-lg', rendered)

    def test_form_validation_for_blank_items(self) -> None:
        """Test form validation for blank items."""
        form = ItemForm(data={"text": ""})
        self.assertFalse(form.is_valid())
        self.assertEqual(form.errors["text"], [EMPTY_ITEM_ERROR])

    def test_form_save_handles_saving_to_a_list(self) -> None:
        """Test form save handles saving to a list."""
        mylist = List.objects.create()
        form = ItemForm(data={"text": "do me"})
        new_item = form.save(for_list=mylist)
        self.assertEqual(new_item, Item.objects.get())
        self.assertEqual(new_item.text, "do me")
        self.assertEqual(new_item.list, mylist)
