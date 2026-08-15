"""Test goat_book."""

import goat_book


def test_import() -> None:
    """Test that the app can be imported."""
    assert isinstance(goat_book.__name__, str)
