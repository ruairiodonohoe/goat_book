"""List models."""

from django.db import models


# Create your models here.
class Item(models.Model):
    """To-Do Item model."""

    text = models.TextField(default="")

    def __str__(self) -> str:
        """Return string representation of the item."""
        return str(self.text)
