"""Tests for CookieStore."""

import os
import sys

import pytest

from py_netatmo_truetemp.cookie_store import CookieStore


class TestCookiePermissions:
    """Tests for cookie file security and permissions."""

    @pytest.mark.skipif(
        sys.platform == "win32", reason="Unix permissions not applicable on Windows"
    )
    def test_cookie_file_created_with_secure_permissions(self, tmp_path):
        """Test that cookie files are created with 0o600 permissions."""
        # Arrange
        cookie_file = tmp_path / "cookies.json"
        store = CookieStore(str(cookie_file))

        # Act: Save cookies
        store.save({"session": "test123", "token": "abc"})

        # Assert: Verify file created
        assert cookie_file.exists()

        # Verify secure permissions (owner read/write only)
        file_mode = os.stat(cookie_file).st_mode & 0o777
        assert file_mode == 0o600, f"Expected 0o600, got {oct(file_mode)}"

    @pytest.mark.skipif(
        sys.platform == "win32", reason="Unix permissions not applicable on Windows"
    )
    def test_parent_directory_created_with_secure_permissions(self, tmp_path):
        """Test that parent directories are created with secure permissions."""
        # Arrange: Nested path that doesn't exist
        cookie_file = tmp_path / "nested" / "path" / "cookies.json"
        store = CookieStore(str(cookie_file))

        # Act: Save cookies (should create parent dirs)
        store.save({"session": "test"})

        # Assert: Verify directories created
        assert cookie_file.parent.exists()

        # Verify directory permissions
        dir_mode = os.stat(cookie_file.parent).st_mode & 0o777
        assert dir_mode == 0o700, f"Expected 0o700, got {oct(dir_mode)}"


class TestCookieOperations:
    """Tests for basic cookie store operations."""

    def test_save_and_load_cookies(self, tmp_path):
        """Test saving and loading cookies."""
        # Arrange
        cookie_file = tmp_path / "cookies.json"
        store = CookieStore(str(cookie_file))
        test_cookies = {"session": "test123", "token": "abc"}

        # Act: Save and load
        store.save(test_cookies)
        loaded = store.load()

        # Assert
        assert loaded == test_cookies

    def test_load_nonexistent_file_returns_none(self, tmp_path):
        """Test loading from nonexistent file returns None."""
        # Arrange
        cookie_file = tmp_path / "nonexistent.json"
        store = CookieStore(str(cookie_file))

        # Act
        result = store.load()

        # Assert
        assert result is None

    def test_clear_removes_cookie_file(self, tmp_path):
        """Test that clear() removes the cookie file."""
        # Arrange
        cookie_file = tmp_path / "cookies.json"
        store = CookieStore(str(cookie_file))
        store.save({"session": "test"})
        assert cookie_file.exists()

        # Act
        store.clear()

        # Assert
        assert not cookie_file.exists()

    def test_clear_nonexistent_file_does_not_error(self, tmp_path):
        """Test that clearing nonexistent file doesn't raise error."""
        # Arrange
        cookie_file = tmp_path / "nonexistent.json"
        store = CookieStore(str(cookie_file))

        # Act & Assert: Should not raise
        store.clear()

    def test_load_corrupt_json_returns_none(self, tmp_path):
        """Test that corrupt JSON file returns None."""
        # Arrange
        cookie_file = tmp_path / "corrupt.json"
        store = CookieStore(str(cookie_file))

        # Write invalid JSON
        with open(cookie_file, "w") as f:
            f.write("{broken json content")

        # Act
        result = store.load()

        # Assert: Should return None and clean up
        assert result is None
        assert not cookie_file.exists()  # Invalid file removed

    def test_load_empty_file_returns_none(self, tmp_path):
        """Test that empty file returns None."""
        # Arrange
        cookie_file = tmp_path / "empty.json"
        store = CookieStore(str(cookie_file))

        # Create empty file
        cookie_file.touch()

        # Act
        result = store.load()

        # Assert
        assert result is None
