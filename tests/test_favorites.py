import json
import pytest
from favorites import Favorites


@pytest.fixture
def favorites_instance(tmpdir):
    # Create a temporary file for testing
    temp_file = tmpdir.join("favorites.json")
    temp_file.write("[]")

    # Create a Favorites instance using the temporary file
    favorites = Favorites()
    favorites.filename = str(temp_file)
    return favorites


def test_initialization(favorites_instance):
    favorites_instance.list = []

    # Check if the favorites list is initialized as an empty list
    assert favorites_instance.list == []


def test_add_movie_to_favorites(favorites_instance):
    movie_id = "123"
    favorites_instance._add(movie_id)

    # Check if the movie ID was added to the favorites list
    assert movie_id in favorites_instance.list


def test_remove_movie():
    favorites = Favorites()
    favorites.list = ['123', '385687', '670292', '695721', '872585', '283871', '1022796']
    favorites._remove("123")
    assert "123" not in favorites.list


def test_update_favorites_add():
    favorites = Favorites()
    favorites.list = ['385687', '670292', '695721', '872585', '283871', '1022796']
    favorites.update("123")
    assert "123" in favorites.list


def test_update_favorites_remove():
    favorites = Favorites()
    favorites.list = ['123', '385687', '670292', '695721', '872585', '283871', '1022796']
    favorites.update("123")
    assert "123" not in favorites.list


def test_save_favorites(tmpdir):
    temp_file = tmpdir.join("favorites.json")
    favorites = Favorites()
    favorites.filename = str(temp_file)

    movie_id = "123"
    favorites._add(movie_id)
    favorites.save()

    # Load the file contents and check if the movie ID is saved
    with open(str(temp_file), 'r', encoding='utf-8') as file:
        data = json.load(file)
        assert movie_id in data
