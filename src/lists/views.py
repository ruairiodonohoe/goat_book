"""List views."""
# Create your views here.

from __future__ import annotations

from typing import TYPE_CHECKING

from django.http import HttpResponse
from django.shortcuts import redirect, render

from lists.models import Item

if TYPE_CHECKING:
    from django.http import HttpRequest, HttpResponse


def home_page(request: HttpRequest) -> HttpResponse:
    """Home page view."""
    if request.method == "POST":
        Item.objects.create(text=request.POST["item_text"])
        return redirect("/lists/the-only-list-in-the-world/")

    items = Item.objects.all()
    return render(request, "home.html", {"items": items})
