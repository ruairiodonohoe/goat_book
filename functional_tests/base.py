"""Test Django homepage."""

import os
import time
from typing import TYPE_CHECKING

from django.contrib.staticfiles.testing import StaticLiveServerTestCase
from selenium import webdriver
from selenium.common.exceptions import WebDriverException
from selenium.webdriver.common.by import By

if TYPE_CHECKING:
    from collections.abc import Callable

MAX_WAIT = 5


class FunctionalTest(StaticLiveServerTestCase):
    """Functional Test Class."""

    @property
    def live_server_url(self) -> str:
        """Return TEST_SERVER env var if set, otherwise fallback to Django's live server."""
        if test_server := os.environ.get("TEST_SERVER"):
            return "http://" + test_server
        return super().live_server_url

    def setUp(self) -> None:
        """Set up test."""
        self.browser = webdriver.Firefox()

    def tearDown(self) -> None:
        """Test down test."""
        self.browser.quit()

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

    def wait_for(self, fn: Callable[[], object]) -> object:
        """Wait for function to complete."""
        start_time = time.time()
        while True:
            try:
                return fn()
            except AssertionError, WebDriverException:
                if time.time() - start_time > MAX_WAIT:
                    raise
                time.sleep(0.5)
