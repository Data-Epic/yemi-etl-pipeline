import pytest
from src.web_scraper import fetch_data, flatten_data, store_moveis_data

def test_fetch_data():
    data = fetch_data()
    assert isinstance(data, dict)
    assert len(data) > 0

def test_flatten_data():
    data = fetch_data()
    flattened_data = flatten_data(data)
    assert flattened_data is not None
    assert isinstance(flattened_data, dict)
    assert len(flattened_data) > 0

def test_store_moveis_data():
    data = store_moveis_data()
    assert isinstance(data, dict)
    assert len(data) > 0