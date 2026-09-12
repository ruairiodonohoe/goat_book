"""Test Django homepage."""

import os
import time
from typing import TYPE_CHECKING, Any

from django.contrib.staticfiles.testing import StaticLiveServerTestCase
from selenium import webdriver
from selenium.common.exceptions import WebDriverException
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys

from functional_tests.container_commands import reset_database

if TYPE_CHECKING:
    from collections.abc import Callable

    from selenium.webdriver.remote.webelement import WebElement

MAX_WAIT = 5


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
        self.browser = webdriver.Firefox()
        self.test_server = os.environ.get("TEST_SERVER")
        if self.test_server:
            self.test_server_url = "http://" + self.test_server
            reset_database(self.test_server)

    def tearDown(self) -> None:
        """Test down test."""
        self.browser.quit()

    def get_item_input_box(self) -> WebElement:
        """Get item input box."""
        return self.browser.find_element(By.ID, "id_text")

    @wait
    def wait_for(self, fn: Callable[[], object]) -> object:
        """Wait for function to complete."""
        return fn()

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
