"""Accounts models."""

import uuid

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


class Token(models.Model):
    """Token class."""

    email = models.EmailField()
    uid = models.CharField(default=uuid.uuid4, max_length=40)

    def __str__(self) -> str:
        """Print string representation."""
        return ""
