"""MyListPage."""

from typing import TYPE_CHECKING

from selenium.webdriver.common.by import By

if TYPE_CHECKING:
    from functional_tests.base import FunctionalTest


class MyListsPage:
    """MyListPage class."""

    def __init__(self, test: FunctionalTest) -> None:
        """Init."""
        self.test = test

    def go_to_my_lists_page(self, email: str) -> MyListsPage:
        """Go to my lists page."""
        self.test.browser.get(self.test.live_server_url)
        self.test.browser.find_element(By.LINK_TEXT, "My lists").click()
        self.test.wait_for(
            lambda: self.test.assertIn(
                email, self.test.browser.find_element(By.TAG_NAME, "h1").text
            )
        )
        return self
