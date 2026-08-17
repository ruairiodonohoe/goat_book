"""List views."""
# Create your views here.

from __future__ import annotations

from typing import TYPE_CHECKING

from django.http import HttpResponse

if TYPE_CHECKING:
    from django.http import HttpRequest


def home_page(request: HttpRequest) -> HttpResponse:
    """Home page view."""
    return HttpResponse("<html><title>To-Do lists</title></html>")
