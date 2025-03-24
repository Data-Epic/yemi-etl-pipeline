import requests
import os
from dotenv import load_dotenv
import json


load_dotenv()
api_key = os.getenv("Rapid_API_KEY")


url = "https://imdb236.p.rapidapi.com/imdb/upcoming-releases"

querystring = {"countryCode": "US", "type": "MOVIE"}

headers = {"x-rapidapi-key": api_key, "x-rapidapi-host": "imdb236.p.rapidapi.com"}


def fetch_data():
    """Fetch data from the API"""
    # This function fetches data from the API and returns it as a JSON object
    try:
        response = requests.request("GET", url, headers=headers, params=querystring)
        return response.json()
    except Exception as e:
        print(f"Error fetching data: {e}")
        return None


def flatten_data(movie_data):
    movies = []
    production_companies = []
    genres = []

    for entry in fetch_data():
        for movie in entry["titles"]:
            movie_record = {
                "id": movie["id"],
                "title": movie["primaryTitle"],
                "original_title": movie["originalTitle"],
                "type": movie["type"],
                "description": movie["description"],
                "primary_image": movie["primaryImage"],
                "content_rating": movie["contentRating"],
                "start_year": movie["startYear"],
                "end_year": movie["endYear"],
                "release_date": movie["releaseDate"],
                "is_adult": movie["isAdult"],
                "runtime_minutes": movie["runtimeMinutes"],
                "average_rating": movie["averageRating"],
                "num_votes": movie["numVotes"],
            }
            movies.append(movie_record)
            if movie.get("productionCompanies"):
                for company in movie.get("productionCompanies", []):
                    production_companies.append(
                        {
                            "id": movie["id"],
                            "company_id": company["id"],
                            "company_name": company["name"]
                        }
                    )
                if movie.get("genres"):
                    for genre in movie["genres"]:
                        genres.append({"id": movie["id"], "genre": genre})
    return {
        "movies": movies,
        "production_companies": production_companies,
        "genres": genres
    }


def store_moveis_data():
    """Fetch top movies from the API"""
    # This function fetches the top movies from the API and returns them as a JSON object
    data = flatten_data(fetch_data())
    folder_path = "data/"
    file_path = os.path.join(folder_path, "movie.json")
    with open(file_path, "w", encoding="utf-8") as f:
        json.dump(data, f, indent=4)
    print("Data stored successfully")


if __name__ == "__main__":
    store_moveis_data()
