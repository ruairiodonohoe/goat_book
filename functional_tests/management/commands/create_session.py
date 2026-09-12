"""Create session."""

from typing import TYPE_CHECKING, Any

if TYPE_CHECKING:
    import argparse

from django.conf import settings
from django.contrib.auth import BACKEND_SESSION_KEY, SESSION_KEY, get_user_model
from django.contrib.sessions.backends.db import SessionStore
from django.core.management.base import BaseCommand

User = get_user_model()


class Command(BaseCommand):
    """Command class."""

    def add_arguments(self, parser: argparse.ArgumentParser) -> None:
        """Add arguments."""
        parser.add_argument("email")

    def handle(self, *_args: Any, **options: Any) -> None:
        """Handle."""
        session_key = create_pre_authenticated_session(options["email"])
        assert session_key is not None
        self.stdout.write(session_key)


def create_pre_authenticated_session(email: str) -> str | None:
    """Create pre_authenticated_session."""
    user, _ = User.objects.get_or_create(email=email)
    session = SessionStore()
    session[SESSION_KEY] = user.pk
    session[BACKEND_SESSION_KEY] = settings.AUTHENTICATION_BACKENDS[0]
    session.save()
    return session.session_key
