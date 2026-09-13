"""Test Django homepage."""

import os
import time
from datetime import UTC, datetime
from typing import TYPE_CHECKING, Any

from django.conf import settings
from django.contrib.staticfiles.testing import StaticLiveServerTestCase
from selenium import webdriver
from selenium.common.exceptions import WebDriverException
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.firefox.options import Options

from functional_tests.container_commands import create_session_on_server, reset_database
from functional_tests.management.commands.create_session import create_pre_authenticated_session

if TYPE_CHECKING:
    from collections.abc import Callable

    from selenium.webdriver.remote.webelement import WebElement
from pathlib import Path

MAX_WAIT = 10
SCREEN_DUMP_LOCATION = Path(__file__).absolute().parent / "screendumps"


def wait(fn: Callable) -> Callable:
    """Wait decorator."""

    def modified_fn(*args: Any, **kwargs: Any) -> None:
        start_time = time.time()
        while True:
            try:
                return fn(*args, **kwargs)
            except AssertionError, WebDriverException:
                if time.time() - start_time > MAX_WAIT:
                    raise
                time.sleep(0.5)

    return modified_fn


class FunctionalTest(StaticLiveServerTestCase):
    """Functional Test Class."""

    def setUp(self) -> None:
        """Set up test."""
        options = Options()
        options.add_argument("--headless")
        self.browser = webdriver.Firefox(options=options)
        self.test_server = os.environ.get("TEST_SERVER")
        if self.test_server:
            self.test_server_url = "http://" + self.test_server
            reset_database(self.test_server)

    def tearDown(self) -> None:
        """Test down test."""
        if self._test_has_failed():
            if not SCREEN_DUMP_LOCATION.exists():
                SCREEN_DUMP_LOCATION.mkdir(parents=True)
            self.take_screenshot()
            self.dump_html()
        self.browser.quit()
        super().tearDown()

    def _test_has_failed(self) -> bool:
        # slightly obscure but couldn't find a better way!
        try:
            return bool(self._outcome.result.failures or self._outcome.result.errors)  # type: ignore  # noqa: PGH003
        except AttributeError:
            return False

    def take_screenshot(self) -> None:
        """Take screenshot."""
        path = SCREEN_DUMP_LOCATION / self._get_filename("png")
        print("screenshotting to", path)  # noqa : T201
        self.browser.get_screenshot_as_file(str(path))

    def dump_html(self) -> None:
        """Dump html."""
        path = SCREEN_DUMP_LOCATION / self._get_filename("html")
        print("dumping page HTML to", path)  # noqa : T201
        path.write_text(self.browser.page_source)

    def _get_filename(self, extension: str) -> str:
        """Get filename."""
        timestamp = datetime.now(UTC).isoformat().replace(":", ".")[:19]
        return f"{self.__class__.__name__}.{self._testMethodName}-{timestamp}.{extension}"

    def get_item_input_box(self) -> WebElement:
        """Get item input box."""
        return self.browser.find_element(By.ID, "id_text")

    @wait
    def wait_for(self, fn: Callable[[], object]) -> object:
        """Wait for function to complete."""
        return fn()

    # Test
    @wait
    def wait_for_row_in_list_table(self, row_text: str) -> None:
        """Check for row in list table."""
        start_time = time.time()
        while True:
            try:
                table = self.browser.find_element(By.ID, "id_list_table")
                rows = table.find_elements(By.TAG_NAME, "tr")
                self.assertIn(row_text, [row.text for row in rows])
            except AssertionError, WebDriverException:
                if time.time() - start_time > MAX_WAIT:
                    raise
                time.sleep(0.5)
            else:
                return

    @wait
    def wait_to_be_logged_in(self, email: str) -> None:
        """Wait to be logged in."""
        self.wait_for(lambda: self.browser.find_element(By.CSS_SELECTOR, "#id_logout"))
        navbar = self.browser.find_element(By.CSS_SELECTOR, ".navbar")
        self.assertIn(email, navbar.text)

    @wait
    def wait_to_be_logged_out(self, email: str) -> None:
        """Wait to be logged out."""
        self.wait_for(lambda: self.browser.find_element(By.CSS_SELECTOR, "input[name=email]"))
        navbar = self.browser.find_element(By.CSS_SELECTOR, ".navbar")
        self.assertNotIn(email, navbar.text)

    def add_list_item(self, item_text: str) -> None:
        """Add list item."""
        num_rows = len(self.browser.find_elements(By.CSS_SELECTOR, "#id_list_table tr"))
        self.get_item_input_box().send_keys(item_text)
        self.get_item_input_box().send_keys(Keys.ENTER)
        item_number = num_rows + 1
        self.wait_for_row_in_list_table(f"{item_number}: {item_text}")

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
