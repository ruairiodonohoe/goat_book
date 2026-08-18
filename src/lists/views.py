"""List views."""
# Create your views here.

from __future__ import annotations

from typing import TYPE_CHECKING

from django.http import HttpResponse
from django.shortcuts import render

if TYPE_CHECKING:
    from django.http import HttpRequest, HttpResponse


def home_page(request: HttpRequest) -> HttpResponse:
    """Home page view."""
    return render(request, "home.html", {"new_item_text": request.POST.get("item_text", "")})
