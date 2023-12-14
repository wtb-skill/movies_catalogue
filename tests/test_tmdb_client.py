import tmdb_client
import pytest
from unittest.mock import Mock
from datetime import datetime


def test_get_poster_url_uses_default_size():
    # Przygotowanie danych
    poster_api_path = "some-poster-path"
    expected_default_size = 'w342'
    # Wywołanie kodu, który testujemy
    poster_url = tmdb_client.get_poster_url(poster_api_path=poster_api_path)
    # Porównanie wyników
    assert expected_default_size in poster_url


def test_get_movies_list(monkeypatch):
    # Lista, którą będzie zwracać przysłonięte "zapytanie do API"
    mock_movies_list = ['Movie 1', 'Movie 2']

    requests_mock = Mock()
    # Wynik wywołania zapytania do API
    response = requests_mock.return_value  # podmieniamy na sztuczną wartość mock
    # Przysłaniamy wynik wywołania metody .json()
    response.json.return_value = mock_movies_list
    monkeypatch.setattr("tmdb_client.requests.get", requests_mock)

    movies_list = tmdb_client.get_movies_list(list_type="popular")
    assert movies_list == mock_movies_list


def test_call_tmdb_api(monkeypatch):
    mock_response = Mock()
    mock_response.json.return_value = {'key': 'value'}
    monkeypatch.setattr('requests.get', lambda url, headers: mock_response)
    result = tmdb_client.call_tmdb_api('some_endpoint')
    assert result == {'key': 'value'}


def test_get_current_date(monkeypatch):
    # Define a mock date for testing purposes
    mock_date = '2023-12-09'  # Set a specific date for testing

    # Mock the datetime.today() method to return a fixed date
    class MockDateTime:
        @classmethod
        def today(cls):
            return datetime.strptime(mock_date, "%Y-%m-%d")

    # Patching the datetime module's datetime class with the MockDateTime class
    monkeypatch.setattr('tmdb_client.datetime', MockDateTime)

    # Call the function being tested
    result = tmdb_client.get_current_date()

    # Assert the result matches the expected mock date
    assert result == mock_date


def test_get_single_movie(monkeypatch):
    # Define a mock response for call_tmdb_api specifically for get_single_movie test
    mock_movie_id = 123
    mock_response = {"id": mock_movie_id, "title": "Sample Movie", "rating": 8.5}

    # Mocking the call_tmdb_api function for this test
    def mock_call_tmdb_api(endpoint):
        # Simulate behavior of call_tmdb_api based on the endpoint
        if endpoint == f"movie/{mock_movie_id}":
            return mock_response
        # If endpoint doesn't match, return None or raise an error based on your function's behavior

    # Patching the call_tmdb_api function with the mock specifically for this test
    monkeypatch.setattr("tmdb_client.call_tmdb_api", mock_call_tmdb_api)

    # Testing get_single_movie function with a specific movie_id
    movie_data = tmdb_client.get_single_movie(mock_movie_id)

    # Asserting that the returned data matches the expected mock response
    assert movie_data == mock_response


def test_get_movies(monkeypatch):
    # Define a mock response for get_movies_list
    mock_list_type = 'popular'
    mock_movies_data = {
        "results": [
            {"id": 1, "title": "Movie 1", "rating": 7.5},
            {"id": 2, "title": "Movie 2", "rating": 8.0},
        ]
    }

    # Mocking the get_movies_list function
    def mock_get_movies_list(list_type):
        if list_type == mock_list_type:
            return mock_movies_data
        # Handle other cases or raise an error if needed

    # Patching the get_movies_list function with the mock
    monkeypatch.setattr("tmdb_client.get_movies_list", mock_get_movies_list)

    # Testing get_movies function with a specific number of movies and list_type
    number_of_movies = 2  # Modify as needed
    movies = tmdb_client.get_movies(number_of_movies, list_type=mock_list_type)

    # Asserting the length of the returned movies matches the expected number_of_movies
    assert len(movies) == number_of_movies
    # You can add more assertions to validate the structure/content of the returned movies list


def test_get_single_movie_cast(monkeypatch):
    # Define a mock response for call_tmdb_api
    mock_movie_id = 123
    mock_cast_data = [
        {"id": 1, "name": "Actor 1", "character": "Character 1"},
        {"id": 2, "name": "Actor 2", "character": "Character 2"},
        # Add more cast data as needed
    ]

    # Mocking the call_tmdb_api function
    def mock_call_tmdb_api(endpoint):
        if endpoint == f"movie/{mock_movie_id}/credits":
            return {"cast": mock_cast_data}
        # Handle other cases or raise an error if needed

    # Patching the call_tmdb_api function with the mock
    monkeypatch.setattr("tmdb_client.call_tmdb_api", mock_call_tmdb_api)

    # Testing get_single_movie_cast function with a specific movie_id
    cast = tmdb_client.get_single_movie_cast(mock_movie_id)

    # Asserting the length of the returned cast matches the length of the mock_cast_data
    assert len(cast) == len(mock_cast_data)
    # You can add more assertions to validate the structure/content of the returned cast list


# List of test cases for capitalize_all_words function
test_cases = [
    ("hello", "Hello"),  # Test case with a single word
    ("hello world", "Hello World"),  # Test case with multiple words
    ("", ""),  # Test case with an empty string
    ("!@# hello world *&^", "!@# Hello World *&^"),  # Test case with special characters
    ("hello123 world456", "Hello123 World456"),  # Test case with numbers
    # Add more test cases as needed
]


# Parametrized pytest using test cases
@pytest.mark.parametrize("input_text, expected_output", test_cases)
def test_capitalize_all_words(input_text, expected_output):
    result = tmdb_client.capitalize_all_words(input_text)
    assert result == expected_output


def test_get_movie_images(monkeypatch):

    def mock_call_tmdb_api(endpoint):
        # Mocking the response for testing purposes
        if "images" in endpoint:
            return {"backdrops": ["image1.jpg", "image2.jpg"], "posters": ["image3.jpg", "image4.jpg"]}
        else:
            return None

    # Patching the call_tmdb_api function with the mock function
    monkeypatch.setattr("tmdb_client.call_tmdb_api", mock_call_tmdb_api)

    # Testing with a sample movie ID
    movie_id = 12345
    images = tmdb_client.get_movie_images(movie_id)

    assert "backdrops" in images
    assert "posters" in images
    assert len(images["backdrops"]) == 2
    assert len(images["posters"]) == 2


def test_search_movie(monkeypatch):

    def mock_call_tmdb_api(endpoint):
        # Mocking the response for testing purposes
        if "search/movie" in endpoint:
            return {
                'results': [
                    {'id': 1, 'title': 'Movie 1'},
                    {'id': 2, 'title': 'Movie 2'},
                ]
            }
        else:
            return None
    # Patching the call_tmdb_api function with the mock function
    monkeypatch.setattr("tmdb_client.call_tmdb_api", mock_call_tmdb_api)

    # Testing with a sample search query
    search_query = "Avengers"  # Replace with an actual search query
    results = tmdb_client.search_movie(search_query)

    assert len(results) == 2  # Ensure that the mocked response has two movies
    assert results[0]['id'] == 1
    assert results[1]['title'] == 'Movie 2'

