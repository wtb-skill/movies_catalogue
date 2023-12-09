import requests
from datetime import datetime

API_KEY = 'a6f2323d004454ac7e351dbbd9392290'
API_TOKEN = 'eyJhbGciOiJIUzI1NiJ9.eyJhdWQiOiJhNmYyMzIzZDAwNDQ1NGFjN2UzNTFkYmJkOTM5MjI5MCIsInN1' \
            'YiI6IjY1NTA5MGZlMmI5MzIwMDlmZTUzNWEzNSIsInNjb3BlcyI6WyJhcGlfcmVhZCJdLCJ2ZXJzaW9uI' \
            'joxfQ.26vl6tYyTUBM4uBMflWTII6SguHeJou487xGT0Hf7Bc'


# src="https://dummyimage.com/300x500/000/fff.jpg"  # blank picture


def get_poster_url(poster_api_path, size="w342"):
    """Tworzy działający adres do obrazka."""
    base_url = "https://image.tmdb.org/t/p/"
    return f"{base_url}{size}/{poster_api_path}"


def get_movies(how_many, list_type='popular'):
    data = get_movies_list(list_type=list_type)
    return data["results"][:how_many]


def get_single_movie(movie_id):
    return call_tmdb_api(f"movie/{movie_id}")


def get_single_movie_cast(movie_id):
    return call_tmdb_api(f"movie/{movie_id}/credits")["cast"]


def get_movies_list(list_type):
    """Zwraca nam pełną listę filmów z wybranej kategorii."""
    return call_tmdb_api(f"movie/{list_type}")


def capitalize_all_words(text):
    return ' '.join(word.capitalize() for word in text.split())


def get_movie_images(movie_id):
    return call_tmdb_api(f"movie/{movie_id}/images")


def search_movie(search_query):
    return call_tmdb_api(f"search/movie?query={search_query}")['results']


def get_tv_series_aired_today(how_many):
    return call_tmdb_api(f"tv/airing_today")['results'][:how_many]


def get_current_date() -> str:
    """Get the current date in a string format (YYYY-MM-DD)."""
    today = str(datetime.today()).split(" ")[0]
    return today


def call_tmdb_api(endpoint):
    full_url = f"https://api.themoviedb.org/3/{endpoint}"
    headers = {
        "Authorization": f"Bearer {API_TOKEN}"
    }
    response = requests.get(full_url, headers=headers)
    response.raise_for_status()
    return response.json()
