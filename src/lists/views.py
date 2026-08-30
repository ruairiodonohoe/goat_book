"""List views."""
# Create your views here.

from __future__ import annotations

from typing import TYPE_CHECKING

from django.core.exceptions import ValidationError
from django.http import HttpResponse
from django.shortcuts import redirect, render

from lists.models import Item, List

if TYPE_CHECKING:
    from django.http import HttpRequest, HttpResponse


def home_page(request: HttpRequest) -> HttpResponse:
    """Home page view."""
    """return render(request, "home.html", {"form": ItemForm()})"""
    return render(request, "home.html")


def view_list(request: HttpRequest, list_id: int) -> HttpResponse:
    """List view."""
    our_list = List.objects.get(id=list_id)
    error = None

    if request.method == "POST":
        try:
            item = Item(text=request.POST["item_text"], list=our_list)
            item.full_clean()
            item.save()
            return redirect(our_list)
        except ValidationError:
            error = "You can't have an empty list item"

    return render(request, "list.html", {"list": our_list, "error": error})


def new_list(request: HttpRequest) -> HttpResponse:
    """Create new list view."""
    nulist = List.objects.create()
    item = Item.objects.create(text=request.POST["item_text"], list=nulist)
    try:
        item.full_clean()
        item.save()
    except ValidationError:
        nulist.delete()
        error = "You can't have an empty list item"
        return render(request, "home.html", {"error": error})
    return redirect(nulist)
