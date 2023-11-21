import requests

API_KEY = 'a6f2323d004454ac7e351dbbd9392290'
API_READ_ACCESS_TOKEN = 'eyJhbGciOiJIUzI1NiJ9.eyJhdWQiOiJhNmYyMzIzZDAwNDQ1NGFjN2UzNTFkYmJkOTM5MjI5MCIsInN1' \
                        'YiI6IjY1NTA5MGZlMmI5MzIwMDlmZTUzNWEzNSIsInNjb3BlcyI6WyJhcGlfcmVhZCJdLCJ2ZXJzaW9uI' \
                        'joxfQ.26vl6tYyTUBM4uBMflWTII6SguHeJou487xGT0Hf7Bc'


def get_popular_movies():
    """
    Zwraca nam pełną listę popularnych filmów.

    :return:
    """
    endpoint = "https://api.themoviedb.org/3/movie/popular"
    api_token = API_READ_ACCESS_TOKEN
    headers = {
        "Authorization": f"Bearer {api_token}"
    }
    response = requests.get(endpoint, headers=headers)
    return response.json()


def get_poster_url(poster_api_path, size="w342"):
    """
    Tworzy działający adres do obrazka.

    :param poster_api_path:
    :param size:
    :return:
    """
    base_url = "https://image.tmdb.org/t/p/"
    return f"{base_url}{size}/{poster_api_path}"


if __name__ == "__main__":
    print(get_popular_movies())
