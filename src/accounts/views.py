"""Accounts views."""

# Create your views here.
from typing import TYPE_CHECKING

from django.contrib import messages
from django.core.mail import send_mail
from django.urls import reverse

if TYPE_CHECKING:
    from django.http import HttpRequest, HttpResponse
from django.shortcuts import redirect

from accounts.models import Token


def send_login_email(request: HttpRequest) -> HttpResponse:
    """Send login email."""
    email = request.POST["email"]
    token = Token.objects.create(email=email)
    url = request.build_absolute_uri(reverse("login") + "?token=" + str(token.uid))
    message_body = f"Use this link to log in:\n\n{url}"
    send_mail(
        "Your login link for Superlists", message_body, "noreply@superlists", ["edith@example.com"]
    )
    messages.success(request, "Check your email, we've sent you a link you can use to log in.")
    return redirect("/")


def login(request: HttpRequest) -> HttpResponse:
    """Login."""
    return redirect("/")
