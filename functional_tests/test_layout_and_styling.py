"""Test Django homepage."""

from selenium.webdriver.common.keys import Keys

from functional_tests.base import FunctionalTest


class LayoutAndStylingTest(FunctionalTest):
    """Tests for layout and styling."""

    def test_layout_and_styling(self) -> None:
        """Test CSS."""
        # Edith goes to the home page
        self.browser.get(self.live_server_url)

        # Her browser window is sup to a very specific size
        self.browser.set_window_size(1024, 768)

        # She notices the input box is nicely centered
        inputbox = self.get_item_input_box()
        self.assertAlmostEqual(inputbox.location["x"] + inputbox.size["width"] / 2, 512, delta=40)

        inputbox.send_keys("testing")
        inputbox.send_keys(Keys.ENTER)
        self.wait_for_row_in_list_table("1: testing")
        inputbox = self.get_item_input_box()
        self.assertAlmostEqual(inputbox.location["x"] + inputbox.size["width"] / 2, 512, delta=40)
