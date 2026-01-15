"""Tests for HomeService."""

import responses
import pytest
from unittest.mock import Mock

from py_netatmo_truetemp.home_service import HomeService
from py_netatmo_truetemp.api_client import NetatmoApiClient
from py_netatmo_truetemp.exceptions import HomeNotFoundError


class TestGetHomesData:
    """Tests for get_homes_data method."""

    @responses.activate
    def test_get_homes_data_success(self, fixture_homesdata_single_home):
        """Test successful retrieval of homes data."""
        # Arrange
        mock_api_client = Mock(spec=NetatmoApiClient)
        mock_api_client.get_typed.return_value = fixture_homesdata_single_home

        home_service = HomeService(mock_api_client)

        # Act
        result = home_service.get_homes_data()

        # Assert
        assert result == fixture_homesdata_single_home
        mock_api_client.get_typed.assert_called_once()

    @responses.activate
    def test_get_homes_data_with_home_id_filter(self, fixture_homesdata_single_home):
        """Test getting homes data with specific home_id filter."""
        # Arrange
        mock_api_client = Mock(spec=NetatmoApiClient)
        mock_api_client.get_typed.return_value = fixture_homesdata_single_home

        home_service = HomeService(mock_api_client)

        # Act
        result = home_service.get_homes_data(home_id="home-123")

        # Assert
        assert result == fixture_homesdata_single_home
        call_args = mock_api_client.get_typed.call_args
        assert call_args[1]["params"]["home_id"] == "home-123"


class TestGetHomeStatus:
    """Tests for get_home_status method."""

    @responses.activate
    def test_get_home_status_success(self, fixture_homestatus_with_temps):
        """Test successful retrieval of home status."""
        # Arrange
        mock_api_client = Mock(spec=NetatmoApiClient)
        mock_api_client.get_typed.return_value = fixture_homestatus_with_temps

        home_service = HomeService(mock_api_client)

        # Act
        result = home_service.get_home_status(home_id="home-123")

        # Assert
        assert result == fixture_homestatus_with_temps
        call_args = mock_api_client.get_typed.call_args
        assert call_args[1]["params"]["home_id"] == "home-123"


class TestGetDefaultHomeId:
    """Tests for get_default_home_id method."""

    def test_get_default_home_id_returns_first_home(
        self, fixture_homesdata_multiple_homes
    ):
        """Test that default home ID is the first home."""
        # Arrange
        mock_api_client = Mock(spec=NetatmoApiClient)
        mock_api_client.get_typed.return_value = fixture_homesdata_multiple_homes

        home_service = HomeService(mock_api_client)

        # Act
        home_id = home_service.get_default_home_id()

        # Assert
        assert home_id == "home-123"  # First home

    def test_get_default_home_id_no_homes_raises_error(self):
        """Test that missing homes raises HomeNotFoundError."""
        # Arrange
        mock_api_client = Mock(spec=NetatmoApiClient)
        mock_api_client.get_typed.return_value = {
            "body": {"homes": []},
            "status": "ok",
        }

        home_service = HomeService(mock_api_client)

        # Act & Assert
        with pytest.raises(HomeNotFoundError, match="No homes found"):
            home_service.get_default_home_id()

    def test_get_default_home_id_malformed_response_raises_error(self):
        """Test that malformed response raises HomeNotFoundError."""
        # Arrange
        mock_api_client = Mock(spec=NetatmoApiClient)
        mock_api_client.get_typed.return_value = {"body": {}}  # Missing 'homes'

        home_service = HomeService(mock_api_client)

        # Act & Assert
        with pytest.raises(HomeNotFoundError):
            home_service.get_default_home_id()
