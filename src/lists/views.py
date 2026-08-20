"""List views."""
# Create your views here.

from __future__ import annotations

from typing import TYPE_CHECKING

from django.http import HttpResponse
from django.shortcuts import redirect, render

from lists.models import Item, List

if TYPE_CHECKING:
    from django.http import HttpRequest, HttpResponse


def home_page(request: HttpRequest) -> HttpResponse:
    """Home page view."""
    return render(request, "home.html")


def view_list(request: HttpRequest, list_id: int) -> HttpResponse:
    """List view."""
    our_list = List.objects.get(id=list_id)
    return render(request, "list.html", {"list": our_list})


def new_list(request: HttpRequest) -> HttpResponse:
    """Create new list view."""
    nulist = List.objects.create()
    Item.objects.create(text=request.POST["item_text"], list=nulist)
    return redirect(f"/lists/{nulist.id}/")


def add_item(request: HttpRequest, list_id: int) -> HttpResponse:
    """Add new item to existing list."""
    our_list = List.objects.get(id=list_id)
    Item.objects.create(text=request.POST["item_text"], list=our_list)
    return redirect(f"/lists/{our_list.id}/")
