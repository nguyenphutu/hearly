from flask import Blueprint, render_template, redirect, abort
from flask_login import login_required, current_user
import bugsnag
from app.models import Movie
from app.models import Categories

home_module = Blueprint('home', __name__, template_folder='templates')

# Index Page When Not Logged In
@home_module.route('/')
def index():
    if current_user.is_authenticated:
        return redirect('/home')
    return render_template('index.html')

# Home Page
@home_module.route('/home')
@login_required
def home_page():
    # movies_1 = Movie.query.filter_by(movie_category=1).limit(24).all()
    # movies_2 = Movie.query.filter_by(movie_category=2).limit(24).all()
    # movies_6 = Movie.query.filter_by(movie_category=6).limit(24).all()
    category = Categories.query.all()
    return render_template('home.html', category=category)
    # return render_template('home.html', action_movies=movies_1, crime_movies=movies_6, adventure_movies=movies_2, current_user=current_user, category=category)


@home_module.route('/detail/<movie_id>', methods=['GET'])
@login_required
def view_detail_movie(movie_id):
    movie = Movie.query.filter_by(movie_id=movie_id).first()
    return render_template('details.html', movie=movie)


@home_module.route('/genres/<genres>')
@login_required
def genres_list(genres):
    category = Categories.query.all()
    genres = Categories.query.filter_by(category_url=genres).first()
    if genres is not None:
        movies = Movie.query.filter_by(movie_category=genres.category_id)
        return render_template('category.html', movies=movies, category_name=genres.category_name, category=category)
    abort(404)


@home_module.route('/search')
@login_required
def search():
    return render_template('search.html')



#Handle Error Not Found
@home_module.errorhandler(404)
def not_found(e):
    return render_template('404.html')