"""Accounts models."""

from django.db import models


# Create your models here.
class User(models.Model):
    """User class."""

    email = models.EmailField(primary_key=True)

    REQUIRED_FIELDS: list[str] = []  # noqa: RUF012
    USERNAME_FIELD = "email"
    is_anonymous = False
    is_authenticated = True

    def __str__(self) -> str:
        """Str representation."""
        return self.email
