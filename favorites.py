import json
from typing import List


class Favorites:
    def __init__(self) -> None:
        self.filename = "static/favorites.json"
        self.list = self._load()

    def _load(self) -> List[str]:
        try:
            with open(self.filename, "r", encoding="utf-8") as file:
                data = json.load(file)
        except FileNotFoundError:
            data = []
        return data

    def save(self) -> None:
        with open(self.filename, 'w', encoding='utf-8') as file:
            json.dump(self.list, file)

    def _add(self, movie_id: str) -> None:
        self.list.append(movie_id)

    def _remove(self, movie_id: str) -> None:
        self.list.remove(movie_id)

    def update(self, movie_id: str) -> None:
        if movie_id in self.list:
            self._remove(movie_id)
        else:
            self._add(movie_id)


