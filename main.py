from flask import Flask, render_template
from tmdb_client import get_poster_url




app = Flask(__name__)


@app.route('/')
def homepage():
    movies = [i for i in range(0, 8)]
    return render_template("homepage.html", movies=movies)


@app.context_processor
def utility_processor():
    def tmdb_image_url(path, size):
        return get_poster_url(path, size)
    return {"tmdb_image_url": tmdb_image_url}


if __name__ == "__main__":
    app.run(debug=True)
