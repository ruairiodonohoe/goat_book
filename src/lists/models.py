"""List models."""

from django.conf import settings
from django.db import models
from django.urls import reverse

# Create your models here.


class List(models.Model):
    """List model."""

    owner = models.ForeignKey(
        "accounts.User", related_name="lists", blank=True, null=True, on_delete=models.CASCADE
    )

    shared_with = models.ManyToManyField(settings.AUTH_USER_MODEL, related_name="shared_lists")

    id: models.AutoField[int, int]

    def __str__(self) -> str:
        """Return string representation of the List."""
        return ""

    def get_absolute_url(self) -> str:
        """Get absolute url."""
        return reverse("view_list", args=[self.id])

    @property
    def name(self) -> None:
        """Name property."""
        return self.item_set.first().text  # type: ignore  # noqa: PGH003


class Item(models.Model):
    """To-Do Item model."""

    text = models.TextField(default="")
    list = models.ForeignKey(List, default=None, on_delete=models.CASCADE)

    class Meta:
        """Class meta of Item."""

        ordering = ("id",)
        unique_together = ("list", "text")

    def __str__(self) -> str:
        """Return string representation of the item."""
        return str(self.text)
