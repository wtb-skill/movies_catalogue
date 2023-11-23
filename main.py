from flask import Flask, render_template, request, redirect, flash
from tmdb_client import get_poster_url, get_movies, get_single_movie, get_single_movie_cast, capitalize_all_words, \
    get_movie_images, search_movie, get_tv_series_aired_today, get_current_date
from random import choice
from favorites import Favorites


app = Flask(__name__)
app.secret_key = 'VERY-SECRET-KEY'


@app.route('/')
def homepage():
    favorites = Favorites()
    allowed_list = ['popular', 'top_rated', 'upcoming', 'now_playing']
    selected_list = request.args.get('list_type', 'popular')

    # Check if the selected_list is in the allowed_list, otherwise default to 'popular'
    if selected_list not in allowed_list:
        selected_list = 'popular'
        incorrect_input = True
    else:
        incorrect_input = False

    movies = get_movies(how_many=8, list_type=selected_list)
    return render_template("homepage.html", movies=movies, list=allowed_list, selected_list=selected_list,
                           incorrect_input=incorrect_input, favorites_list=favorites.list)


@app.context_processor
def utility_processor():
    def tmdb_image_url(path, size):
        return get_poster_url(path, size)
    return {"tmdb_image_url": tmdb_image_url}


@app.route("/movie/<movie_id>")
def movie_details(movie_id):
    movie = get_single_movie(movie_id)
    cast = get_single_movie_cast(movie_id)[:12]
    movie_images = get_movie_images(movie_id)
    if movie_images['backdrops']:
        selected_backdrop = choice(movie_images['backdrops'])
    else:
        selected_backdrop = []
    return render_template("movie_details.html", movie=movie, cast=cast, selected_backdrop=selected_backdrop)


@app.template_filter('capitalize_all_words')
def capitalize_all_words_filter(s):
    return capitalize_all_words(s)


@app.route("/search")
def search():
    favorites = Favorites()
    search_query = request.args.get("q", "")
    if search_query:
        movies = search_movie(search_query=search_query)
    else:
        movies = []
    return render_template("search.html", movies=movies, search_query=search_query, favorites_list=favorites.list)


@app.route("/today")
def tv_series_aired():
    today = get_current_date()
    tv_series = get_tv_series_aired_today(how_many=20)
    return render_template("today.html", tv_series=tv_series, today=today)


@app.route("/favorites/add", methods=['POST'])
def add_to_favorites():
    data = request.form
    movie_id = data.get('movie_id')
    movie_title = data.get('movie_title')
    if movie_id and movie_title:
        favorites = Favorites()
        favorites.update(movie_id=movie_id)
        favorites.save()
        flash(f"The Favorites list has been updated with a title '{movie_title}!'")
    return redirect(request.referrer or '/')


@app.route("/favorites")
def show_favorites():
    favorites = Favorites()
    if favorites:
        movies = []
        for movie_id in favorites.list:
            _movie_details = get_single_movie(movie_id)
            movies.append(_movie_details)
    else:
        movies = []
    return render_template("favorites.html", movies=movies, favorites_list=favorites.list)


if __name__ == "__main__":
    app.run(debug=True)
