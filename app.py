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
# Recipes homepage - get recipes by various categories
@app.route("/recipes")
def recipes():
    # Save queried data in variable 'recipes'
    recipes = mongo.db.recipes.find()
    # Render template 'recipes.html',
    # and make 'recipes' data available for template
    return render_template("recipes.html", recipes=recipes)


# Meals page - get recipes ordered by meals
@app.route("/meals")
def meals():
    return render_template("meals.html")


# Cuisine page - get recipes ordered by cuisines
@app.route("/cuisines")
def cuisines():
    return render_template("cuisines.html")


# Ingredient page - get recipes ordered by ingredients
@app.route("/ingredients")
def ingredients():
    return render_template("ingredients.html")


# Diets page - get recipes ordered by diets
@app.route("/diets")
def diets():
    return render_template("diets.html")


# User profile view - my_recipe
@app.route("/my_recipes")
def my_recipes():
    return render_template("my_recipes.html")


# User login page
@app.route("/login")
def login():
    return render_template("login.html")


# Registration of new user
@app.route("/register", methods=["GET", "POST"])
def register():
    # validate if method in register.html is 'POST"
    if request.method == "POST":
        # get username from mongodb in lowercase
        existing_user = mongo.db.users.find_one(
            {"username": request.form.get("username").lower()})

        # if user exist
        if existing_user:
            # show flash message
            flash("Username already exists")
            # and redirect visitor to the register page
            return redirect(url_for("register"))

        # create variable 'register'
        register = {
            # and store 'username and password from form
            "username": request.form.get("username").lower(),
            # using werkzeug to generate password salt and randomize stored password
            "password": generate_password_hash(request.form.get("password"))
        }
        # insert variable 'register' in 'users' collection on mongodb
        mongo.db.users.insert_one(register)

        # put the new user into 'session' cookie named 'user' on the browser
        session["user"] = request.form.get("username").lower()
        # give success feedback to user
        flash("Registration Successful!")
        # redirect user to profile page
        return redirect(url_for("profile", username=session["user"]))

    # by default - render register.html template
    return render_template("register.html")


# Run Flask application
# Get IP and PORT number and run Flask application in debug mode
if __name__ == "__main__":
    app.run(host=os.environ.get("IP"),
            port=int(os.environ.get("PORT")),
            debug=True)
