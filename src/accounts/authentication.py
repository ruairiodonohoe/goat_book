"""Authentication."""

import sys
from typing import TYPE_CHECKING, Any

from django.contrib.auth.backends import BaseBackend

if TYPE_CHECKING:
    from django.http import HttpRequest

from accounts.models import ListUser, Token


class PasswordlessAuthenticationBackend(BaseBackend):
    """PasswordlessAuthenticationBackend class."""

    def authenticate(
        self,
        request: HttpRequest | None,  # noqa : ARG002
        uid: str | None = None,
        **kwargs: Any,  # noqa : ARG002
    ) -> ListUser | None:
        """Authenticate."""
        print("uid", uid, file=sys.stderr)  # noqa: T201
        if not Token.objects.filter(uid=uid).exists():
            print("no token found", file=sys.stderr)  # noqa: T201
            return None
        token = Token.objects.get(uid=uid)
        print("got token", file=sys.stderr)  # noqa: T201
        try:
            user = ListUser.objects.get(email=token.email)

        except ListUser.DoesNotExist:
            print("new user", file=sys.stderr)  # noqa: T201
            return ListUser.objects.create(email=token.email)
        else:
            print("got user", file=sys.stderr)  # noqa: T201
            return user

    def get_user(self, user_id: str, email: str | None = None) -> ListUser | None:  # noqa: ARG002
        """Get user."""
        return ListUser.objects.get(email=email)
