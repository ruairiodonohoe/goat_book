"""Forms."""

from typing import Any

from django import forms

from lists.models import Item, List

EMPTY_ITEM_ERROR = "You can't have an empty list item"
DUPLICATE_ITEM_ERROR = "You've already got this in your list"


class ItemForm(forms.Form):
    """Item Forms."""

    text = forms.CharField(error_messages={"required": EMPTY_ITEM_ERROR}, required=True)

    def save(self, for_list: List) -> Item:
        """Save Item to List."""
        return Item.objects.create(list=for_list, text=self.cleaned_data["text"])


class ExistingListItemForm(ItemForm):
    """Existing List Item Form."""

    def __init__(self, for_list: List, *args: Any, **kwargs: Any) -> None:
        super().__init__(*args, **kwargs)
        self._for_list = for_list

    def clean_text(self) -> str:
        """Clean text."""
        text = self.cleaned_data["text"]
        if Item.objects.filter(list=self._for_list, text=text).exists():
            raise forms.ValidationError(DUPLICATE_ITEM_ERROR)
        return text

    def save(self, for_list: List | None = None) -> Item:
        """Save."""
        target_list = for_list if for_list is not None else self._for_list
        return Item.objects.create(list=target_list, text=self.cleaned_data["text"])
