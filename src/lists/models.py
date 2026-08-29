"""List models."""

from django.db import models
from django.urls import reverse

# Create your models here.


class List(models.Model):
    """List model."""

    id: models.AutoField[int, int]

    def __str__(self) -> str:
        """Return string representation of the List."""
        return ""

    def get_absolute_url(self) -> str:
        """Get absolute url."""
        return reverse("view_list", args=[self.id])


class Item(models.Model):
    """To-Do Item model."""

    text = models.TextField(default="")
    list = models.ForeignKey(List, default=None, on_delete=models.CASCADE)

    def __str__(self) -> str:
        """Return string representation of the item."""
        return str(self.text)
