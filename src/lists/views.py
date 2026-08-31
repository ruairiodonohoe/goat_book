"""List views."""
# Create your views here.

from __future__ import annotations

from typing import TYPE_CHECKING

from django.http import HttpResponse
from django.shortcuts import redirect, render

from lists.forms import ItemForm
from lists.models import List

if TYPE_CHECKING:
    from django.http import HttpRequest, HttpResponse


def home_page(request: HttpRequest) -> HttpResponse:
    """Home page view."""
    """return render(request, "home.html")"""
    return render(request, "home.html", {"form": ItemForm()})


def view_list(request: HttpRequest, list_id: int) -> HttpResponse:
    """List view."""
    our_list = List.objects.get(id=list_id)
    form = ItemForm()

    if request.method == "POST":
        form = ItemForm(data=request.POST)
        if form.is_valid():
            form.save(for_list=our_list)
            return redirect(our_list)

    return render(request, "list.html", {"list": our_list, "form": form})


def new_list(request: HttpRequest) -> HttpResponse:
    """Create new list view."""
    form = ItemForm(data=request.POST)
    if form.is_valid():
        nulist = List.objects.create()
        form.save(for_list=nulist)
        return redirect(nulist)

    return render(request, "home.html", {"form": form})
