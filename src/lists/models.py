"""List models."""

from django.db import models

# Create your models here.


class List(models.Model):
    """List model."""

    def __str__(self) -> str:
        """Return string representation of the List."""
        return ""


class Item(models.Model):
    """To-Do Item model."""

    text = models.TextField(default="")
    list = models.ForeignKey(List, default=None, on_delete=models.CASCADE)

    def __str__(self) -> str:
        """Return string representation of the item."""
        return str(self.text)
