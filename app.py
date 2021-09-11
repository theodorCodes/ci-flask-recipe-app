# ------------------------------------------------------------------------------
# Dependencies
import os
from flask import (
    Flask, flash, render_template, redirect, request, session, url_for
)
from flask_pymongo import PyMongo
from bson.objectid import ObjectId
from werkzeug.security import generate_password_hash, check_password_hash

# import content from env.py file if available
if os.path.exists("env.py"):
    import env


# Flask instance
app = Flask(__name__)

# DB connection - Save env.py credentials in config of app instance
app.config["MONGO_DBNAME"] = os.environ.get("MONGO_DBNAME")
app.config["MONGO_URI"] = os.environ.get("MONGO_URI")
app.secret_key = os.environ.get("SECRET_KEY")

# PyMongo instance, taking 'app' as parameter
mongo = PyMongo(app)


# Base url
@app.route("/")
# Homepage
@app.route("/recipes")
def recipes():
    # Save queried data in variable 'recipes'
    recipes = mongo.db.recipes.find()
    # Render template 'recipes.html',
    # and make 'recipes' data available for template
    return render_template("recipes.html", recipes=recipes)


# Meals page
@app.route("/meals")
def meals():
    return render_template("meals.html")


# Cuisine page
@app.route("/cuisines")
def cuisines():
    return render_template("cuisines.html")


# Cuisine page
@app.route("/ingredients")
def ingredients():
    return render_template("ingredients.html")


# Cuisine page
@app.route("/diets")
def diets():
    return render_template("diets.html")


# Login page
@app.route("/login")
def login():
    return render_template("login.html")


# User - register
@app.route("/register", methods=["GET", "POST"])
def register():
    if request.method == "POST":
        # check if username already exists in db
        existing_user = mongo.db.users.find_one(
            {"username": request.form.get("username").lower()})

        # redirect visitor to the register page
        if existing_user:
            flash("Username already exists")
            return redirect(url_for("register"))

        # store username and password from form of register.html
        # in variable register
        register = {
            "username": request.form.get("username").lower(),
            "password": generate_password_hash(request.form.get("password"))
        }
        # insert variable 'register' in 'users' collection
        mongo.db.users.insert_one(register)

        # put the new user into 'session' cookie
        session["user"] = request.form.get("username").lower()
        flash("Registration Successful!")
        # ADDING REDIRECT TO OUR NEW USER PROFILE PAGE HERE
        return redirect(url_for("profile", username=session["user"]))

    # render register.html template
    return render_template("register.html")


# User - profile /my_recipe view
@app.route("/my_recipes")
def my_recipes():
    return render_template("my_recipes.html")


# Get IP and PORT number and run Flask application in debug mode
if __name__ == "__main__":
    app.run(host=os.environ.get("IP"),
            port=int(os.environ.get("PORT")),
            debug=True)
