import os
from flask import (
    Flask, flash, render_template,
    redirect, request, session, url_for)
from flask_pymongo import PyMongo
from bson.objectid import ObjectId
from werkzeug.security import generate_password_hash, check_password_hash
if os.path.exists("env.py"):
    import env


app = Flask(__name__)

app.config["MONGO_DBNAME"] = os.environ.get("MONGO_DBNAME")
app.config["MONGO_URI"] = os.environ.get("MONGO_URI")
app.secret_key = os.environ.get("SECRET_KEY")

mongo = PyMongo(app)


@app.route("/")
@app.route("/get_records")
def get_records():
    records = list(mongo.db.records.find())
    return render_template("records.html", records=records)


@app.route("/signup", methods=["GET", "POST"])
def signup():
    if request.method == "POST":
        # check if username already exists in db
        existing_user = mongo.db.users.find_one(
            {"username": request.form.get("username").lower()})

        if existing_user:
            flash("Username already exists")
            return redirect(url_for("signup"))

        signup = {
            "username": request.form.get("username").lower(),
            "password": generate_password_hash(request.form.get("password"))
        }
        mongo.db.users.insert_one(signup)

        # put the new user into 'session' cookie
        session["user"] = request.form.get("username").lower()
        flash("Sign-Up Complete!")
        return redirect(url_for("profile", username=session["user"]))

    return render_template("sign-up.html")


@app.route("/login", methods=["GET", "POST"])
def login():
    if request.method == "POST":
        # check if username exists in db
        existing_user = mongo.db.users.find_one(
            {"username": request.form.get("username").lower()})

        if existing_user:
            # ensure hashed password matches user input
            if check_password_hash(
                existing_user["password"], request.form.get("password")):
                    session["user"] = request.form.get("username").lower()
                    flash("Welcome, {}".format(
                        request.form.get("username")))
                    return redirect(url_for(
                        "profile", username=session["user"]))
            else:
                # invalid password match
                flash("Incorrect Username and/or Password")
                return redirect(url_for("login"))

        else:
            # username doesn't exist
            flash("Incorrect Username and/or Password")
            return redirect(url_for("login"))

    return render_template("login.html")


@app.route("/profile/<username>", methods=["GET", "POST"])
def profile(username):
    # grab the session user's username from db
    username = mongo.db.users.find_one(
        {"username": session["user"]})["username"]

    records = mongo.db.records.find({"user": username})
    trading = mongo.db.trading.find().sort("trading_position", 1)
    genres = mongo.db.genres.find().sort("genre", 1)
    return render_template("profile.html", username=username, records=records, genres=genres)


@app.route("/logout")
def logout():
    # remove user from session cookie
    flash("You have been logged out")
    session.pop("user")
    return redirect(url_for("login"))


@app.route("/new_record", methods=["GET", "POST"])
def new_record():
    if request.method == "POST":
        record = {
            "trading_position": request.form.get("trading_position"),
            "album_name": request.form.get("album_name"),
            "artist_name": request.form.get("artist_name"),
            "genre": request.form.get("genre"),
            "release_date": request.form.get("release_date"),
            "release_date": request.form.get("release_date"),
            "price": request.form.get("price"),
            "contact": request.form.get("contact"),
            "user": session["user"]        
        }
        mongo.db.records.insert_one(record)
        flash("Record Successfully Added")
        return redirect(url_for("get_records"))
        
    trading = mongo.db.trading.find().sort("trading_position", 1)
    genres = mongo.db.genres.find().sort("genre", 1)
    return render_template("new_record.html", trading=trading, genres=genres)


@app.route("/edit_record/<record_id>", methods=["GET", "POST"])
def edit_record(record_id):

    if request.method == "POST":
        submit = {
            "trading_position": request.form.get("trading_position"),
            "album_name": request.form.get("album_name"),
            "artist_name": request.form.get("artist_name"),
            "genre": request.form.get("genre"),
            "release_date": request.form.get("release_date"),
            "release_date": request.form.get("release_date"),
            "price": request.form.get("price"),
            "contact": request.form.get("contact"),
            "user": session["user"]          
        }
        mongo.db.records.update_one({"_id": ObjectId(record_id)}, {"$set": submit })
        flash("Record Updated")

    record = mongo.db.records.find_one({"_id": ObjectId(record_id)})
    trading = mongo.db.trading.find().sort("trading_position", 1)
    genres = mongo.db.genres.find().sort("genre", 1)
    return render_template("edit_record.html", record=record, trading=trading, genres=genres)


@app.route("/delete_record/<record_id>")
def delete_record(record_id):
    mongo.db.records.delete_one({"_id": ObjectId(record_id)})
    flash("Record Deleted")
    return redirect(url_for("get_records"))


if __name__ == "__main__":
    app.run(host=os.environ.get("IP"),
            port=int(os.environ.get("PORT")),
            debug=os.environ.get("DEBUG", False))
