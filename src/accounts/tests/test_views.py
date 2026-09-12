"""Test accounts views."""

from unittest.mock import MagicMock, patch

from django.test import TestCase

from accounts.models import Token


class SendLoginEmailViewTest(TestCase):
    """SendLoginEmailViewTest Class."""

    def test_redirects_to_home_page(self) -> None:
        """Test redirects to home page."""
        response = self.client.post(
            "/accounts/send_login_email", data={"email": "edith@example.com"}
        )
        self.assertRedirects(response, "/")

    @patch("accounts.views.send_mail")
    def test_sends_mail_to_address_from_post(self, mock_send_mail: MagicMock) -> None:
        """Test sends mail to address from post."""
        self.client.post("/accounts/send_login_email", data={"email": "edith@example.com"})
        self.assertEqual(mock_send_mail.called, True)
        (subject, _body, from_email, to_list), _kwargs = mock_send_mail.call_args
        self.assertEqual(subject, "Your login link for Superlists")
        self.assertEqual(from_email, "noreply@superlists")
        self.assertEqual(to_list, ["edith@example.com"])

    def test_adds_success_message(self) -> None:
        """Test adds success message."""
        response = self.client.post(
            "/accounts/send_login_email", data={"email": "edith@example.com"}, follow=True
        )
        message = next(iter(response.context["messages"]))
        self.assertEqual(
            message.message, "Check your email, we've sent you a link you can use to log in."
        )
        self.assertEqual(message.tags, "success")

    def test_creates_token_associated_with_email(self) -> None:
        """Test creates token associated with email."""
        self.client.post("/accounts/send_login_email", data={"email": "edith@example.com"})
        token = Token.objects.get()
        self.assertEqual(token.email, "edith@example.com")

    @patch("accounts.views.send_mail")
    def test_sends_link_to_login_using_token_uid(self, mock_send_mail: MagicMock) -> None:
        """Test sends link to login using token uid."""
        self.client.post("/accounts/send_login_email", data={"email": "edith@example.com"})
        token = Token.objects.get()
        expected_url = f"http://testserver/accounts/login?token={token.uid}"
        (_subject, body, _from_email, _to_list), _kwargs = mock_send_mail.call_args
        self.assertIn(expected_url, body)


class LoginViewTest(TestCase):
    """LoginViewTest class."""

    def test_redirects_to_home_page(self) -> None:
        """Test redirects to home page."""
        response = self.client.get("/accounts/login?token=abcd123")
        self.assertRedirects(response, "/")
