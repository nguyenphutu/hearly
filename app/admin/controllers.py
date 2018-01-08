import cloudinary
import os
from cloudinary.uploader import upload
from cloudinary.utils import cloudinary_url
from flask import Blueprint, Flask, render_template, request, redirect, make_response
from flask_login import login_required, current_user
from sqlalchemy import exc
from werkzeug.utils import secure_filename

from app import app
from app.helpers.decorators import require_admin
from app.models import Categories, db, Movie

ALLOWED_EXTENSIONS = set(['srt'])


def allowed_file(filename):
    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS


cloudinary.config(
    cloud_name="hearly",
    api_key="745842632146681",
    api_secret="IsdqcBnEc1b_NszRdHH5pm3RDI8"
)

admin = Blueprint('admin', __name__, url_prefix='/admin', template_folder='templates')


@admin.route('/')
@admin.route('/movie', methods=['GET', 'POST'])
@login_required
@require_admin
def movie():
    movies = Movie.query.all()
    return render_template("list_movie.html", movies=movies, current_user=current_user)


@admin.route('/sub', methods=['GET', 'POST'])
@login_required
@require_admin
def movie_sub():
    movies = Movie.query.all()
    return render_template("list_sub.html", movies=movies)


@admin.route('/category', methods=['GET', 'POST'])
@login_required
@require_admin
def category():
    cates = Categories.query.all()
    return render_template("list_cate.html", Cates=cates)

@admin.route('/sub/download/<subfile>', methods=['GET', 'POST'])
@login_required
@require_admin
def download(subfile):
     file = os.path.join(app.config['UPLOAD_FOLDER'], subfile + ".srt")
     headers = {"Content-Disposition": "attachment; filename=%s.srt" % subfile}
     with open(file, 'r') as f:
         body = f.read()
     return make_response((body, headers))


@admin.route('/upload', methods=['GET', 'POST'])
@login_required
def upload_movie():
    Cates = Categories.query.all()
    if request.method == 'GET':
        return render_template("upload_movie.html", Cates=Cates)

    cates = request.form.getlist('cate')
    #categori = Categories.query.filter_by(category_name=cate1).first()

    if ('file_image' not in request.files) or (request.files["file_image"].filename == ''):
        Flask(" you not choose file_image !!!")
        return render_template("upload_movie.html", Cates=Cates)

    url1, url2 = upload_image(request.files['file_image'])

    if 'srt_file' not in request.files:
        Flask(" you not choose srt_file !!!")
        return render_template("upload_movie.html", Cates=Cates)

    file = request.files['srt_file']

    if file.filename == '':
        Flask(" filename not null ")
        return render_template("upload_movie.html", Cates=Cates)
    if file and allowed_file(file.filename):
        filename = secure_filename(file.filename)
        file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))

    try:
        movie = Movie(movie_id=request.form['movie_id'].strip(), movie_thumbnail=url1, movie_thumbnail2=url2,
                      movie_name=request.form['movie_name'].strip(),
                      movie_description=request.form['movie_decription'].strip())

        if cates is not None:
            for cate in cates:
                categori = Categories.query.filter_by(category_name=cate).first()
                movie.category.append(categori)
        db.session.add(movie)
        db.session.commit()
    except exc.IntegrityError:
        db.session.rollback()
        return 'ERROR! movie_id ({}) already exists.'.format(request.form['movie_id'])
    return redirect('/admin')


@admin.route('/movie/edit/<movie_id>', methods=['GET', 'POST'])
@admin.route('/edit/<movie_id>', methods=['GET', 'POST'])
@login_required
@require_admin
def edit_movie(movie_id):
    movie = Movie.query.filter_by(movie_id=movie_id).first()
    Cates = Categories.query.all()
    catelist = movie.category;
    if request.method == 'GET':
        return render_template("movie.html", Cates=Cates, movie=movie, catelist = catelist)

    cates = request.form.getlist('cate')
    #categori = Categories.query.filter_by(category_name=cate).first()

    if ('file_image' not in request.files) or (request.files["file_image"].filename == ''):
        Flask(" you not change file_image !!!")
        url1, url2 = None, None
    else:
        url1, url2 = upload_image(request.files['file_image'])

    # if 'srt_file' not in request.files and request.files['srt_file'].filename == '':
    #     Flask(" you not change srt_file !!!")
    #     return render_template("movie.html", Cates=Cates, movie=movie)
    #
    # file = request.files['srt_file']
    #
    # if file and allowed_file(file.filename):
    #     filename = secure_filename(file.filename)
    #     file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
    try:
        movie.movie_id = request.form['movie_id'].strip()
        if url1 is not None:
            movie.movie_thumbnail = url1
            movie.movie_thumbnail2 = url2
        movie.movie_name = request.form['movie_name'].strip()
        movie.movie_description = request.form['movie_decription'].strip()
        if cates is not None:
            for cate in cates:
                categori = Categories.query.filter_by(category_name=cate).first()
                movie.category.append(categori)
        db.session.commit()
    except exc.IntegrityError:
        db.session.rollback()
        return 'ERROR! movie_id ({}) has error update.'.format(request.form['movie_id'])
    return redirect("/admin")


@admin.route('/movie/delete/<movie_id>')
@admin.route('/delete/<movie_id>')
@login_required
@require_admin
def delete_movie(movie_id):
    movie = Movie.query.filter_by(movie_id=movie_id).first()
    if movie is None:
        return 'ERROR! movie_id ({}) not exists.'.format(movie_id)
    try:
        db.session.delete(movie)
        db.session.commit()
        os.remove(os.path.join(app.config['UPLOAD_FOLDER'], (movie_id + '.srt')))
    except exc.IntegrityError:
        db.session.rollback()
        return 'ERROR! movie_id ({}) can not delete'.format(request.form['movie_id'])
    return redirect('/admin')


@admin.route('/movie/search', methods=['GET', 'POST'])
@admin.route('/search', methods=['GET', 'POST'])
@login_required
@require_admin
def search():
    if request.method == "POST":
        movie_id = request.form['search'].strip()
        movie = Movie.query.filter_by(movie_id=movie_id).first()
        return render_template("adsearch.html", movie=movie)
    if request.args.get("search"):
        movie_id = request.args.get("search")
        movie = Movie.query.filter_by(movie_id=movie_id).first()
        return render_template("adsearch.html", movie=movie)
    else:
        return render_template("adsearch.html")


def upload_image(files):
    # Config
    upload_result = upload(files)
    thumbnail_url1, options = cloudinary_url(upload_result['public_id'], format="jpg", crop="scale", secure=True)
    thumbnail_url2, options = cloudinary_url(upload_result['public_id'], format="jpg", crop="scale", secure=True)
    return thumbnail_url1, thumbnail_url2
