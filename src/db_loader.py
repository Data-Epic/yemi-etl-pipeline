from sqlalchemy import (
    create_engine,
    Column,
    Integer,
    String,
    Date,
    Float,
    Boolean,
    ForeignKey,
)
from sqlalchemy.orm import sessionmaker, relationship
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import Table

base = declarative_base()


class Movies(base):
    __tablename__ = "movies"

    id = Column(String, primary_key=True)
    original_title = Column(String)
    type = Column(String)
    description = Column(String)
    primary_image = Column(String)
    content_rating = Column(String)
    start_year = Column(Integer)
    end_year = Column(Integer)
    release_date = Column(Date)
    genres = Column(String)
    is_adult = Column(Boolean)
    runtime_minutes = Column(Integer)
    average_rating = Column(Float)
    num_votes = Column(Integer)
    company_id = Column(String)
    company_name = Column(String)

    genre = relationship("Genre", secondary="movie_genre", back_populates="movies")
    production_company = relationship("ProductionCompany", back_populates="movies")

    def __repr__(self, primary_title, release_date):
        self.primary_title = primary_title
        self.release_date = release_date
        return f"<Movies(primary_title={self.primary_title}, release_date={self.release_date})>"


class Genre(base):
    __tablename__ = "genre"

    id = Column(Integer, primary_key=True, autoincrement=True)
    genre = Column(String)
    movies = relationship("Movies", secondary="movie_genre", back_populates="genre")

    def __repr__(self, genre):
        self.genre = genre
        return f"<Genre(genre={self.genre})>"


class ProductionCompany(base):
    __tablename__ = "production_company"

    id = Column(String, primary_key=True)
    company_name = Column(String)
    company_id = Column(String)
    movie_id = Column(String, ForeignKey("movies.id"))
    movies = relationship("Movies", back_populates="production_company")

    def __repr__(self, company):
        self.company = company
        return f"<ProductionCompany(company={self.company})>"


# defining Many-toMany relationship between Movies and Genre
movie_genre = Table(
    "movie_genre",
    base.metadata,
    Column("movie_id", String, ForeignKey("movies.id")),
    Column("genre_id", Integer, ForeignKey("genre.id")),
)


class Database:
    def __init__(self, db_name="harrythedataknight"):
        self.engine = create_engine(
            f"postgresql://postgres:{db_name}@localhost:5432/movies_db"
        )
        self.Session = sessionmaker(bind=self.engine)
        self.session = self.Session()
        base.metadata.create_all(self.engine)

    def add_data(self, data="data/movies.csv"):
        import polars as pl

        df = pl.read_csv(data)

        # Inserting data into the Movies table
        for row in df.iter_rows(named=True):
            movie = Movies(
                id=row["id"],
                original_title=row["original_title"],
                type=row["type"],
                description=row["description"],
                primary_image=row["primary_image"],
                content_rating=row["content_rating"],
                start_year=row["start_year"],
                end_year=row["end_year"],
                release_date=row["release_date"],
                genres=row["genre"],
                is_adult=row["is_adult"],
                runtime_minutes=row["runtime_minutes"],
                average_rating=row["average_rating"],
                num_votes=row["num_votes"],
                company_id=row["company_id"],
                company_name=row["company_name"],
            )
            self.session.add(movie)

        # Inserting data inot the genre table
        for row in df.iter_rows(named=True):
            genre = Genre(genre=row["genre"])
            self.session.add(genre)

        # Inserting data into the production_company table
        for row in df.iter_rows(named=True):
            production_company = ProductionCompany(
                id=row["id"],
                company_name=row["company_name"],
                company_id=row["company_id"],
            )
            self.session.add(production_company)
        print(
            "Data uploaded successfully into Movies, Genre and ProductionCompany tables"
        )

    def get_data(self):
        return self.session.query(Movies).all()

    def close(self):
        self.session.commit()
        self.session.close()


if __name__ == "__main__":
    db = Database()
    db.add_data()
    db.close()
# Compare this snippet from src/data_transform.py
# # Compare this snippet from src/data_transform.py:


# database_url = 'postgresql://postgres:harrythedataknight@localhost:5432/movies_db'
# engine = create_engine(database_url, echo=True)
# Session = sessionmaker(bind=engine)
# session = Session()
# base.metadata.create_all(engine)
# base.metadata.drop_all(engine)  # Drops all tables
