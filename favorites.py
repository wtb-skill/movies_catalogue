import json


class Favorites:
    def __init__(self):
        self.filename = "static/favorites.json"
        self.list = self._load()

    def _load(self):
        try:
            with open(self.filename, "r", encoding="utf-8") as file:
                data = json.load(file)
        except FileNotFoundError:
            data = []
        return data

    def save(self):
        with open(self.filename, 'w', encoding='utf-8') as file:
            json.dump(self.list, file)

    def _add(self, movie_id: str):
        self.list.append(movie_id)

    def _remove(self, movie_id: str):
        self.list.remove(movie_id)

    def update(self, movie_id: str):
        if movie_id in self.list:
            self._remove(movie_id)
        else:
            self._add(movie_id)


