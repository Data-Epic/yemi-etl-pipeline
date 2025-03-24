import pytest
import polars as pl
from src.data_transform import transfrom_data

@pytest.fixture
def sample_data():
    data = {
        "id": ["tt12345", "tt67890", "tt11111"],
        "title": ["Movie A", "Movie B", "Movie C"],
        "start_year": [2023, None, 2025],
        "end_year": [None, None, 2030],
        "runtime_minutes": [120, None, 90],
        "num_votes": [1000, 2000, None],
        "average_rating": [8.0, None, 7.5],
        "release_date": ["2024-05-01", None, "2025-10-15"],
        "genre": ["Action", "Comedy", None],
    }
    return pl.DataFrame(data)

def test_replace_nulls(sample_data):
    """Test if null values in integer columns are replaced with 0."""
    transformed_df = transfrom_data(sample_data)
    assert transformed_df["start_year"].null_count() == 0
    assert transformed_df["end_year"].null_count() == 0
    assert transformed_df["runtime_minutes"].null_count() == 0
    assert transformed_df["num_votes"].null_count() == 0
    assert transformed_df["average_rating"].null_count() == 0

def test_unique_ids(sample_data):
    """Test if transformed data have unique movie IDs."""
    transformed_df = transfrom_data(sample_data)
    assert transformed_df["id"].n_unique() == transformed_df.height  #

def test_date_conversion(sample_data):
    """Test if release_date is correctly converted to datetime format."""
    transformed_df = transfrom_data(sample_data)
    assert transformed_df["release_date"].dtype == pl.Date  
