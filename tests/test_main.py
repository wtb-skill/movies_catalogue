import pytest
from main import app
from unittest.mock import Mock


@pytest.fixture
def client():
    app.config['TESTING'] = True
    with app.test_client() as client:
        yield client


def test_homepage(client):
    response = client.get('/')
    assert response.status_code == 200


def test_movie_details(client):
    response = client.get('/movie/123')
    assert response.status_code == 200


def test_search(client):
    response = client.get('/search?q=Avengers')
    assert response.status_code == 200


def test_tv_series_aired(client):
    response = client.get('/today')
    assert response.status_code == 200


def test_add_to_favorites(client):
    response = client.post('/favorites/add', data={'movie_id': '123', 'movie_title': 'Test Movie'})
    assert response.status_code == 302  # Redirect status code


def test_show_favorites(client):
    response = client.get('/favorites')
    assert response.status_code == 200


@pytest.fixture
def tmdb_api_mock():
    return Mock(return_value={'results': []})


def test_homepage_with_different_list_types(monkeypatch, tmdb_api_mock):
    monkeypatch.setattr("tmdb_client.call_tmdb_api", tmdb_api_mock)

    list_types = ['popular', 'top_rated', 'upcoming', 'now_playing']

    with app.test_client() as client:
        for list_type in list_types:
            response = client.get(f'/?list_type={list_type}')
            assert response.status_code == 200
            tmdb_api_mock.assert_called_once_with(f'movie/{list_type}')
            tmdb_api_mock.reset_mock()  # Reset mock to ensure clean state for the next iteration

