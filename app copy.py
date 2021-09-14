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


# ------------------------------------------------------------------------------
# Base url
@app.route("/")
# ------------------------------------------------------------------------------
# Recipes homepage - get recipes by various categories
@app.route("/recipes")
def recipes():
    # Save queried data in variable 'recipes'
    recipes = mongo.db.recipes.find()
    # Render template 'recipes.html',
    # and make 'recipes' data available for template
    return render_template("recipes.html", recipes=recipes)


# ------------------------------------------------------------------------------
# Meals page - get recipes ordered by meals
@app.route("/meals")
def meals():
    return render_template("meals.html")


# ------------------------------------------------------------------------------
# Cuisine page - get recipes ordered by cuisines
@app.route("/cuisines")
def cuisines():
    return render_template("cuisines.html")


# ------------------------------------------------------------------------------
# Ingredient page - get recipes ordered by ingredients
@app.route("/ingredients")
def ingredients():
    return render_template("ingredients.html")


# ------------------------------------------------------------------------------
# Diets page - get recipes ordered by diets
@app.route("/diets")
def diets():
    return render_template("diets.html")


# ------------------------------------------------------------------------------
# Registration of new user
@ app.route("/register", methods=["GET", "POST"])
def register():
    # validate if method in register.html is 'POST"
    if request.method == "POST":
        # get username from mongodb
        # and validate with username in lowercase from form
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
            # and store username from input in lowercase
            "username": request.form.get("username").lower(),
            # user email
            "email": request.form.get("email").lower(),
            # password from form using werkzeug to generate password salt
            "password": generate_password_hash(request.form.get("password"))
        }
        # insert variable 'register' in 'users' collection on mongodb
        mongo.db.users.insert_one(register)
        # put the new user into 'session' cookie named 'user' on the browser
        session["user"] = request.form.get("username").lower()
        # give success feedback to user
        flash("Registration Successful!")
        # redirect user to my_recipes page
        return redirect(url_for("my_recipes", username=session["user"]))

    # by default - render register.html template
    return render_template("register.html")


# ------------------------------------------------------------------------------
# User login page
@ app.route("/login", methods=["GET", "POST"])
def login():
    # validate if method is 'POST'
    if request.method == "POST":
        # get username from mongodb and store in 'existing_user'
        # and validate with 'username' in lowercase from form
        existing_user = mongo.db.users.find_one(
            {"username": request.form.get("username").lower()})
        # if username from form is equal to users found on mongodb
        if existing_user:
            # check salted password using werkzeug, comparing both passwords
            # the hashed password from stored in db and the password from input
            if check_password_hash(
                    existing_user["password"], request.form.get("password")):
                # create session cookie for username
                session["user"] = request.form.get("username").lower()
                # send message with user stored username from input
                flash("Hi {}, Welcome back to Daily Delights".format(
                    request.form.get("username")))
                # redirect user to my_recipes page
                return redirect(url_for("my_recipes", username=session["user"]))
            # if the password is invalid
            else:
                # send this message to visitor
                flash("Your Username and/or Password does not match")
                # and redirect visitor back to the login page
                return redirect(url_for("login"))
        # if the user does not exist
        else:
            # send the same message to visitor
            flash("Your Username and/or Password does not match")
            # and redirect visitor back to the login page
            return redirect(url_for("login"))

    return render_template("login.html")


# ------------------------------------------------------------------------------
# User - recipe page
# passing through username as route
@app.route("/my_recipes/<username>", methods=["GET", "POST"])
# and passing username here as argument
def my_recipes(username):
    # in variable 'username', store queried user information from username
    # that is stored in session cookie
    username = mongo.db.users.find_one(
        {"username": session["user"]})["username"]
    # if session cookie truthy,
    # then render my_recipes.html with the username information
    if session["user"]:
        return render_template("my_recipes.html", username=username)
    # if not truthy, redirect visitor to login page
    return redirect(url_for("login"))
    # from here, we can store the username cookie as menu link in base.html
    # to ensure that only identified users can load their profile


# ------------------------------------------------------------------------------
# User - profile page
# passing through username as route
@app.route("/profile/<username>", methods=["GET", "POST"])
# and passing username as argument
def profile(username):
    # in variable 'username', store queried user information username that is
    # stored in session cookie, specifying to only receive ["username"] value
    # username = mongo.db.users.find_one(
    #     {"username": session["user"]})["username"]

    # get user profile

    user_profile = mongo.db.users.find_one(
        {"_id":  0, "username": session["user"], "email": 1})
    print(user_profile)
    # if session cookie truthy,
    # then render profile.html with the username information
    if session["user"]:
        return render_template("profile.html", username=user_profile)
    # if not truthy, redirect visitor to login page
    return redirect(url_for("login"))
    # from here, we can store the username cookie as menu link in base.html
    # to ensure that only identified users can load their profile


# ------------------------------------------------------------------------------
# User logout
@app.route("/logout")
def logout():
    # logout message
    flash("You have been logged out")
    # remove 'user' session cookie
    session.pop("user")
    # return to login page
    return redirect(url_for("login"))


# ------------------------------------------------------------------------------
# Run Flask application
# Get IP and PORT number and run Flask application in debug mode
if __name__ == "__main__":
    app.run(host=os.environ.get("IP"),
            port=int(os.environ.get("PORT")),
            debug=True)
