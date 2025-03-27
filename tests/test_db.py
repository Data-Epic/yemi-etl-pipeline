import pytest
from unittest.mock import patch
from sqlalchemy.exc import OperationalError
from src.db_loader import Database, Movies, Genre


def test_database_initialization():
    """Test if the database initializes correctly."""
    try:
        db = Database(db_name="harrythedataknight")
        assert db.engine is not None
        assert db.session is not None
    except OperationalError:
        pytest.fail("Database connection failed.")


def test_movie_has_genre_relationship():
    """Test that a Movie instance can be assigned a Genre."""
    movie = Movies(id="tt12345", original_title="Sample Movie")
    genre = Genre(id=1, genre="Action")

    # Simulate the relationship
    movie.genre.append(genre)

    assert genre in movie.genre
    assert movie in genre.movies


def test_get_data():
    """Test if data retrieval works correctly."""
    db = Database(db_name="harrythedataknight")
    movies = db.get_data()

    assert isinstance(movies, list)
    assert all(isinstance(movie, Movies) for movie in movies)

    db.close()
