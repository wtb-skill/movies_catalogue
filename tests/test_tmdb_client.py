import tmdb_client
from unittest.mock import Mock


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
