import requests
from datetime import datetime

API_KEY = 'a6f2323d004454ac7e351dbbd9392290'
API_TOKEN = 'eyJhbGciOiJIUzI1NiJ9.eyJhdWQiOiJhNmYyMzIzZDAwNDQ1NGFjN2UzNTFkYmJkOTM5MjI5MCIsInN1' \
            'YiI6IjY1NTA5MGZlMmI5MzIwMDlmZTUzNWEzNSIsInNjb3BlcyI6WyJhcGlfcmVhZCJdLCJ2ZXJzaW9uI' \
            'joxfQ.26vl6tYyTUBM4uBMflWTII6SguHeJou487xGT0Hf7Bc'


# src="https://dummyimage.com/300x500/000/fff.jpg"  # blank picture


def get_poster_url(poster_api_path, size="w342"):
    """
    Tworzy działający adres do obrazka.

    :param poster_api_path:
    :param size:
    :return:
    """
    base_url = "https://image.tmdb.org/t/p/"
    return f"{base_url}{size}/{poster_api_path}"


def get_movies(how_many, list_type='popular'):
    data = get_movies_list(list_type=list_type)
    return data["results"][:how_many]


def get_single_movie(movie_id):
    endpoint = f"https://api.themoviedb.org/3/movie/{movie_id}"
    headers = {
        "Authorization": f"Bearer {API_TOKEN}"
    }
    response = requests.get(endpoint, headers=headers)
    return response.json()


def get_single_movie_cast(movie_id):
    endpoint = f"https://api.themoviedb.org/3/movie/{movie_id}/credits"
    headers = {
        "Authorization": f"Bearer {API_TOKEN}"
    }
    response = requests.get(endpoint, headers=headers)
    return response.json()["cast"]


def get_movies_list(list_type):
    """
    Zwraca nam pełną listę filmów z wybranej kategorii.

    :return:
    """
    endpoint = f"https://api.themoviedb.org/3/movie/{list_type}"
    headers = {
        "Authorization": f"Bearer {API_TOKEN}"
    }
    response = requests.get(endpoint, headers=headers)
    return response.json()


def capitalize_all_words(text):
    return ' '.join(word.capitalize() for word in text.split())


def get_movie_images(movie_id):
    endpoint = f"https://api.themoviedb.org/3/movie/{movie_id}/images"
    headers = {
        "Authorization": f"Bearer {API_TOKEN}"
    }
    response = requests.get(endpoint, headers=headers)
    return response.json()


def search_movie(search_query):
    endpoint = f"https://api.themoviedb.org/3/search/movie?query={search_query}"
    headers = {
        "Authorization": f"Bearer {API_TOKEN}"
    }
    response = requests.get(endpoint, headers=headers)
    response = response.json()
    return response['results']


def get_tv_series_aired_today(how_many):
    endpoint = "https://api.themoviedb.org/3/tv/airing_today"
    headers = {
        "Authorization": f"Bearer {API_TOKEN}"
    }
    response = requests.get(endpoint, headers=headers)
    response = response.json()
    return response['results'][:how_many]


def get_current_date() -> str:
    """Get the current date in a string format (YYYY-MM-DD)."""
    today = str(datetime.today()).split(" ")[0]
    return today


if __name__ == "__main__":
    print(get_current_date())
