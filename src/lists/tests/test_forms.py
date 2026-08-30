"""Tests for Forms."""

from django.test import TestCase

from lists.forms import EMPTY_ITEM_ERROR, ItemForm


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
