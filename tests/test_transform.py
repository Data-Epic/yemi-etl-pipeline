import pytest
from src.data_transform import transfrom_data

def test_transfrom():
    data = {"id": 1, "name": "John"}, {"id": 2, "name": "Doe"}
    data = transfrom_data(data)
    assert "id" in data.columns

def test_clean_data_empty():
    # data = transfrom_data()
    clean = transfrom_data({})
    assert len(clean) == 0

def test_missing_data():
    data = [{"id": 1, "name": "John"}, {"id": 2}]
    clean = transfrom_data(data)
    assert len(clean) == 1
