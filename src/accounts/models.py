"""Accounts models."""

from django.contrib.auth.models import AbstractBaseUser, BaseUserManager
from django.db import models


# Create your models here.
class Token(models.Model):
    """Token class."""

    email = models.EmailField()
    uid = models.CharField(max_length=255)

    def __str__(self) -> str:
        """Return a readable representation for the Token."""
        return f"{self.email} ({self.uid})"


class ListUserManager(BaseUserManager):
    """ListUserManager Class."""

    def create_user(self, email: str) -> None:
        """Create user."""
        ListUser.objects.create(email=email)

    def create_superuser(self, email: str) -> None:
        # def create_superuser(self, email: str, password: str) -> None:
        """Create superuser."""
        self.create_user(email)


class ListUser(AbstractBaseUser):
    """ListUser Class."""

    email = models.EmailField(primary_key=True)
    USERNAME_FIELD = "email"

    # REQUIRED_FIELDS = ['email', 'height'] #noqa: ERA001
    objects = ListUserManager()

    @property
    def is_staff(self) -> bool:
        """Check is staff."""
        return self.email == "harry.percival@example.com"

    @property
    def is_active(self) -> bool:
        """Check is active."""
        return True
