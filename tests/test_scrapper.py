import pytest
from unittest.mock import patch, MagicMock, mock_open
import json
import os
from src.web_scraper import fetch_data, flatten_data, store_moveis_data


@patch("requests.request")
def test_fetch_data(mock_request):
    mock_response = MagicMock()
    mock_response.json.return_value = {"titles": [{"id": "tt12345", "primaryTitle": "Test Movie"}]}
    mock_request.return_value = mock_response

    data = fetch_data()
    assert isinstance(data, dict)
    assert "titles" in data

@patch("requests.request")
def test_fetch_data_empty_response(mock_request):
    mock_response = MagicMock()
    mock_response.json.return_value = {}  
    mock_request.return_value = mock_response

    data = fetch_data()
    assert isinstance(data, dict)  # Should still return a dictionary
    assert not data  # Should be an empty dictionary

@patch("builtins.open", new_callable=mock_open)
@patch("os.path.join", return_value="test_movie.json")
def test_store_movies_data(mock_path_join, mock_file):
    """Test store_movies_data creates a JSON file with expected structure."""
    with patch("json.dump") as mock_json_dump:
        store_moveis_data()
        mock_file.assert_called_once_with("test_movie.json", "w", encoding="utf-8")
        mock_json_dump.assert_called()
