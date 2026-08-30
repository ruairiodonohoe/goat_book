"""Forms."""

from typing import ClassVar

from django import forms

from lists.models import Item

EMPTY_ITEM_ERROR = "You can't have an empty list item"


class ItemForm(forms.models.ModelForm):
    """Item Forms."""

    class Meta:
        """Meta for ItemForm."""

        model = Item
        fields = ("text",)
        widgets: ClassVar[dict] = {
            "text": forms.widgets.TextInput(
                attrs={"placeholder": "Enter a to-do item", "class": "form-control form-control-lg"}
            )
        }
        error_messages: ClassVar[dict] = {"text": {"required": EMPTY_ITEM_ERROR}}

    # item_text = forms.CharField( #noqa: ERA001
    #     widget=forms.widgets.TextInput( #noqa: ERA001
    #         attrs={"placeholder": "Enter a to-do item", "class":
    #  "form-control form-control-lg"}
    #     ) #noqa: ERA001
    # ) #noqa: ERA001
