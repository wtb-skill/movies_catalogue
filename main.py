from flask import Flask, render_template, request
from tmdb_client import get_poster_url, get_movies, get_single_movie, get_single_movie_cast, capitalize_all_words


app = Flask(__name__)


@app.route('/')
def homepage():
    allowed_list = ['top_rated', 'upcoming', 'popular', 'now_playing']
    selected_list = request.args.get('list_type', 'popular')

    # Check if the selected_list is in the allowed_list, otherwise default to 'popular'
    if selected_list not in allowed_list:
        selected_list = 'popular'
        incorrect_input = True
    else:
        incorrect_input = False

    movies = get_movies(how_many=8, list_type=selected_list)
    return render_template("homepage.html", movies=movies, list=allowed_list, selected_list=selected_list, incorrect_input=incorrect_input)


@app.context_processor
def utility_processor():
    def tmdb_image_url(path, size):
        return get_poster_url(path, size)
    return {"tmdb_image_url": tmdb_image_url}


@app.route("/movie/<movie_id>")
def movie_details(movie_id):
    movie = get_single_movie(movie_id)
    cast = get_single_movie_cast(movie_id)[:12]
    return render_template("movie_details.html", movie=movie, cast=cast)


@app.template_filter('capitalize_all_words')
def capitalize_all_words_filter(s):
    return capitalize_all_words(s)


if __name__ == "__main__":
    app.run(debug=True)
