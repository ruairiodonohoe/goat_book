"""My List functional tests."""

from django.conf import settings
from django.contrib.auth import get_user_model

from functional_tests.base import FunctionalTest
from functional_tests.container_commands import create_session_on_server
from functional_tests.management.commands.create_session import create_pre_authenticated_session

User = get_user_model()


class MyListsTest(FunctionalTest):
    """MyListTest class."""

    def create_pre_authenticated_session(self, email: str) -> None:
        """Create pre authenticated session."""
        if (
            self.test_server
            and "localhost" not in self.test_server
            and "127.0.01" not in self.test_server
        ):
            session_key = create_session_on_server(self.test_server, email)
        else:
            session_key = create_pre_authenticated_session(email)

        self.browser.get(self.live_server_url + "/404_no_such_url/")
        self.browser.add_cookie(
            {"name": settings.SESSION_COOKIE_NAME, "value": session_key, "path": "/"}
        )

    def test_logged_in_users_lists_are_saved_as_my_lists(self) -> None:
        """Test logged in users lists are saved as my lists."""
        email = "edith@example.com"
        self.browser.get(self.live_server_url)
        self.wait_to_be_logged_out(email)

        # Edith is a logged-in user
        self.create_pre_authenticated_session(email)
        self.browser.get(self.live_server_url)
        self.wait_to_be_logged_in(email)
