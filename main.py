from flask import render_template, request, redirect, url_for, jsonify, make_response
from models import app, db, login_manager, bcrypt
from models.user import User
from models.liked import Likes
from flask_login import login_user, login_required, logout_user, current_user
import requests 

# GET requests

@app.route("/home")
def home():
    headers = {"accept": "application/json",
              "Authorization": "Bearer eyJhbGciOiJIUzI1NiJ9.eyJhdWQiOiJmNzRjMzE3NWJjMGExNzNiMDkwZjkyZTljMjQ3NzRmNyIsInN1YiI6IjY0NzBlM2NmNzcwNzAwMDBkZjE0MDFjYiIsInNjb3BlcyI6WyJhcGlfcmVhZCJdLCJ2ZXJzaW9uIjoxfQ.Y3zfcONHo2VXJV_CQbXmR56Kw0YqR296Bvqz_HbcbGU"}
    
    #POPULAR
    url = "https://api.themoviedb.org/3/movie/popular?language=en-US&page=1"
    response = requests.get(url, headers=headers)

    #TOP_RATED
    urlP = "https://api.themoviedb.org/3/movie/top_rated?language=en-US&page=1"
    responseP = requests.get(urlP, headers=headers)

    #UPCOMING
    urlU = "https://api.themoviedb.org/3/movie/upcoming?language=en-US&page=1"
    responseU = requests.get(urlU, headers=headers)
  
    if response.status_code == 200:
        data_popular = response.json()["results"]
        data_rated = responseP.json()["results"]
        data_upcoming = responseU.json()["results"]

        return render_template("index.html", items_popular=data_popular, items_rated=data_rated, items_upcoming=data_upcoming)

    return render_template("index.html")     

@app.route("/liked", methods=["GET", "POST"])
def liked():
    data = request.json
    if current_user.is_authenticated:
        author_id = current_user.id
        if data.get("liked"):
            l = Likes(data.get("id"), data.get("name"), author_id)
            db.session.add(l)
            db.session.commit()
            print("ADDED")
        elif data.get("liked") == False:
            l = Likes.query.filter_by(movie_id = data.get("id"), author_id = author_id).first()
            db.session.delete(l)
            db.session.commit()
            print("DELETED")
        else:
            return make_response("liked not found", 400)

    return jsonify({"id": "123"})

@app.route("/home/history")
def history():
    return render_template("history.html")

@app.route("/home/series")
def series():
    return render_template("series.html")

@app.route("/home/tvshow")
def tv():
    return render_template("tvshow.html")

@app.route("/profile")
@login_required
def profile():
    headers = {"accept": "application/json",
              "Authorization": "Bearer eyJhbGciOiJIUzI1NiJ9.eyJhdWQiOiJmNzRjMzE3NWJjMGExNzNiMDkwZjkyZTljMjQ3NzRmNyIsInN1YiI6IjY0NzBlM2NmNzcwNzAwMDBkZjE0MDFjYiIsInNjb3BlcyI6WyJhcGlfcmVhZCJdLCJ2ZXJzaW9uIjoxfQ.Y3zfcONHo2VXJV_CQbXmR56Kw0YqR296Bvqz_HbcbGU"}
    
    movies = current_user._like
    print(movies)
    data_list = []
    for film in movies:
        url = f"https://api.themoviedb.org/3/movie/{film.movie_id}?language=en-US"
        response = requests.get(url, headers=headers)
        if response.status_code == 200:
            data_list.append(response.json())

    return render_template("profile.html", data_list=data_list)

@app.route("/search", methods=["POST", "GET"])
def search():
    if request.method == "POST":
        data = request.form.get("search")
        url = f"https://api.themoviedb.org/3/search/movie?query={data}"
        headers = {"accept": "application/json",
              "Authorization": "Bearer eyJhbGciOiJIUzI1NiJ9.eyJhdWQiOiJmNzRjMzE3NWJjMGExNzNiMDkwZjkyZTljMjQ3NzRmNyIsInN1YiI6IjY0NzBlM2NmNzcwNzAwMDBkZjE0MDFjYiIsInNjb3BlcyI6WyJhcGlfcmVhZCJdLCJ2ZXJzaW9uIjoxfQ.Y3zfcONHo2VXJV_CQbXmR56Kw0YqR296Bvqz_HbcbGU"}
        if len(data) == 0:
            return render_template("search.html")
        response = requests.get(url, headers=headers)

        if response.status_code == 200:
            search_data = response.json()["results"]
            return render_template("search.html", results = search_data)
        
    return render_template("search.html")

@app.route("/settings")
def settings():
    return render_template("settings.html")

@app.route("/home/toprated")
def rating():
    url = "https://api.themoviedb.org/3/movie/top_rated?language=en-US&page=1"
    headers = {"accept": "application/json",
              "Authorization": "Bearer eyJhbGciOiJIUzI1NiJ9.eyJhdWQiOiJmNzRjMzE3NWJjMGExNzNiMDkwZjkyZTljMjQ3NzRmNyIsInN1YiI6IjY0NzBlM2NmNzcwNzAwMDBkZjE0MDFjYiIsInNjb3BlcyI6WyJhcGlfcmVhZCJdLCJ2ZXJzaW9uIjoxfQ.Y3zfcONHo2VXJV_CQbXmR56Kw0YqR296Bvqz_HbcbGU"}
    response = requests.get(url, headers=headers)
    print(response.status_code)

    if response.status_code == 200:
        data = response.json()["results"]

        return render_template("tranding.html", items=data)

    return render_template("rating.html")

@app.route("/home/upcoming")
def upcoming():
    url = "https://api.themoviedb.org/3/movie/upcoming?language=en-US&page=1"
    headers = {"accept": "application/json",
              "Authorization": "Bearer eyJhbGciOiJIUzI1NiJ9.eyJhdWQiOiJmNzRjMzE3NWJjMGExNzNiMDkwZjkyZTljMjQ3NzRmNyIsInN1YiI6IjY0NzBlM2NmNzcwNzAwMDBkZjE0MDFjYiIsInNjb3BlcyI6WyJhcGlfcmVhZCJdLCJ2ZXJzaW9uIjoxfQ.Y3zfcONHo2VXJV_CQbXmR56Kw0YqR296Bvqz_HbcbGU"}
    response = requests.get(url, headers=headers)
    print(response.status_code)

    if response.status_code == 200:
        data = response.json()["results"]

        return render_template("tranding.html", items=data)

    return render_template("rating.html")

@app.route("/home/tranding")
def tranding():
    url = "https://api.themoviedb.org/3/movie/popular?language=en-US&page=1"
    headers = {"accept": "application/json",
              "Authorization": "Bearer eyJhbGciOiJIUzI1NiJ9.eyJhdWQiOiJmNzRjMzE3NWJjMGExNzNiMDkwZjkyZTljMjQ3NzRmNyIsInN1YiI6IjY0NzBlM2NmNzcwNzAwMDBkZjE0MDFjYiIsInNjb3BlcyI6WyJhcGlfcmVhZCJdLCJ2ZXJzaW9uIjoxfQ.Y3zfcONHo2VXJV_CQbXmR56Kw0YqR296Bvqz_HbcbGU"}
    response = requests.get(url, headers=headers)

    if response.status_code == 200:
        data = response.json()["results"]

        return render_template("tranding.html", items=data)

    return render_template("tranding.html")

@app.route("/movie/<int:id>")
def movie(id):
    url = f"https://api.themoviedb.org/3/movie/{id}?language=en-US"
    video_url=f"https://api.themoviedb.org/3/movie/{id}/videos?language=en-US"
    headers = {"accept": "application/json",
              "Authorization": "Bearer eyJhbGciOiJIUzI1NiJ9.eyJhdWQiOiJmNzRjMzE3NWJjMGExNzNiMDkwZjkyZTljMjQ3NzRmNyIsInN1YiI6IjY0NzBlM2NmNzcwNzAwMDBkZjE0MDFjYiIsInNjb3BlcyI6WyJhcGlfcmVhZCJdLCJ2ZXJzaW9uIjoxfQ.Y3zfcONHo2VXJV_CQbXmR56Kw0YqR296Bvqz_HbcbGU"}
    response = requests.get(url, headers=headers)

    urlR = f"https://api.themoviedb.org/3/movie/{id}/recommendations?language=en-US&page=1"
    responseR = requests.get(urlR, headers=headers)

    video = requests.get(video_url, headers=headers)
    video_data = video.json().get("results")
    # print(response.status_code)
    like_status = False

    if current_user.is_authenticated:
        author_id = current_user.id
        if Likes.query.filter_by(movie_id=id, author_id=author_id).first():
            like_status = True

    if response.status_code == 200 and video.status_code == 200 and responseR.status_code == 200:
        video_key=video_data[0]['key'] if len(video_data) >= 1 else None
        recommended_data = responseR.json().get("results")[0:4]
        data = response.json()

        return render_template("movie.html", item=data, like_status=like_status, video=video_key, recommended = recommended_data)

    return render_template("movie.html") 

# POST, GET requests

@app.route("/registration", methods=["GET", "POST"])
def registration():
    if request.method == "POST":      
        if request.form.get("check1") == "off" and request.form.get("check2") == "off":
            return render_template("registration.html", exep={"error": "Invalid checkbox"})
        
        name = request.form.get("name")
        surname = request.form.get("surname")
        password = request.form.get("password")
        email = request.form.get("email")
        
        try:
            user = User(name, surname, email, password)
            user.password = bcrypt.generate_password_hash(password).decode("utf8")
            db.session.add(user)
            db.session.commit()
            print(User.query.all())
            login_user(user)
            return redirect(url_for("home"))
        except Exception as e:
            return render_template("registration.html", exep=e.args[0])
    
    return render_template("registration.html", exep={})

@login_manager.user_loader
def load_user(user_id):
    return User.query.get(user_id)

@login_manager.unauthorized_handler
def unauthorized():
    return redirect(url_for("registration"))

@app.route("/login", methods=["POST", "GET"])
def login():
    if request.method == "POST":
        email = request.form.get("email")
        password = request.form.get("password")
        try:
            user = User.query.filter_by(_email = email).first()
            if not user:
                return render_template("login.html", exep={"error": "Invalid email"})
            if not bcrypt.check_password_hash(user._password, password):
                return render_template("login.html", exep={"error": "Invalid password"})
            login_user(user, remember = True)
            return redirect(url_for("home"))
        except Exception as e:
            return render_template("login.html", exep=e.args[0])
        except any as e:
            print(e)

        
    return render_template("login.html", exep={})

@app.route("/logout")
def logout():
    logout_user()
    return redirect(url_for("home"))

# POST, GET requests

with app.app_context():
    db.create_all()

app.run(debug=True)