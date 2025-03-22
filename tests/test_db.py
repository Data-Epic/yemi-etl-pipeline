import pytest
from sqlalchemy.orm import sessionmaker
from src.db_loader import Database, Movies

@pytest.fixture(scope="module")
def test_db():
    db = Database(db_name="test_db")
    yield db
    db.close()

@pytest.fixture
def session(test_db):
    session = test_db.Session()
    yield session
    session.rollback()  # Reset changes

def test_movies_table_empty(session):
    assert session.query(Movies).count() == 0
