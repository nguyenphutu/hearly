from flask import Blueprint, render_template, abort
from flask_login import login_required
import bugsnag
from app.helpers.parseSubtitles import convert_srt
from app.models import Movie

watch = Blueprint('watch', __name__, url_prefix='/watch', template_folder='templates')


# Dynamic movies
@watch.route('/<movie_id>', methods=['GET'])
@login_required
def get_movie_id(movie_id):
    movie = Movie.query.filter_by(movie_id=movie_id).first()
    if movie is not None:
        try:
            return render_template('player.html', movie_name=movie.movie_name, movie_id=movie_id,
                                   subtitles=convert_srt("app/watch/subtitles/" + movie_id + ".srt"))
        except FileNotFoundError:
            bugsnag.notify(
                movie.movie_name + ' with id ' + movie.movie_id + ' subtitles file error or not found')
            abort(404)
    else:
        abort(404)
