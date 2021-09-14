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
# Recipe details page


# ------------------------------------------------------------------------------
# User registration page
@ app.route("/register", methods=["GET", "POST"])
def register():
    # validate if method in register.html is 'POST"
    if request.method == "POST":
        # get email from mongodb
        # and validate with email from form input
        existing_user = mongo.db.users.find_one(
            {"email": request.form.get("email").lower()})
        # if user already exists
        if existing_user:
            # show flash message
            flash("Email already exists")
            # and redirect visitor to the register page
            return redirect(url_for("register"))
        # if user does not exists, create variable 'register'
        register = {
            # and store username from input in lowercase,
            "username": request.form.get("username").lower(),
            # user email
            "email": request.form.get("email").lower(),
            # and password from form using werkzeug to generate password salt
            "password": generate_password_hash(request.form.get("password"))
        }
        # insert variable 'register' in 'users' collection on mongodb
        # AND store created user info in '_id' variable
        _id = mongo.db.users.insert_one(register)
        # create session cookie with inserted_id
        # and convert the bson object into a string value
        session["user"] = str(_id.inserted_id)
        print(session["user"])
        # get user name for greeting message
        user = mongo.db.users.find_one(
            {"_id": ObjectId(session["user"])}, {"password": 0})
        # give success feedback to user
        flash("Registration Successful!")
        # redirect user to my_recipes page and passing through username to my_recipe.html
        return redirect(url_for("my_recipes", username=user['username']))

    # by default - render register.html template
    return render_template("register.html")


# ------------------------------------------------------------------------------
# User login page
@ app.route("/login", methods=["GET", "POST"])
def login():
    # validate if method is 'POST'
    if request.method == "POST":
        # get email from mongodb and store in 'existing_user'
        # and validate with email from form input
        existing_user = mongo.db.users.find_one(
            {"email": request.form.get("email").lower()})
        # if email from form is equal to user email found on mongodb
        if existing_user:
            # check salted password using werkzeug, comparing both passwords
            # the hashed password stored on db and the password from input
            if check_password_hash(
                    existing_user["password"], request.form.get("password")):
                # create session cookie for user with username
                session["user"] = existing_user["username"].lower()

                # TEST 1 (works) create session cookie  with id
                # user_id = existing_user["_id"]
                # print(user_id)

                # TEST 2 ()
                # session["profile"] = str(existing_user["_id"])

                # send message with user stored username
                flash("Hi {}, Welcome back to Daily Delights".format(
                    existing_user["username"].lower()))
                return redirect(url_for("my_recipes", username=session["user"]))
                # redirect user to my_recipes page
            # if the password is invalid
            else:
                # send this message to visitor
                flash("Your Email and/or Password does not match")
                # and redirect visitor back to the login page
                return redirect(url_for("login"))
        # if the user does not exist
        else:
            # send the same message to visitor
            flash("Your Email and/or Password does not match")
            # and redirect visitor back to the login page
            return redirect(url_for("login"))

    return render_template("login.html")


# ------------------------------------------------------------------------------
# User profile, my_recipes page
# with username as route, preventing visitors without cookie to see this page
@ app.route("/my_recipes/<username>", methods=["GET", "POST"])
# and passing username here as argument
def my_recipes(username):
    # in variable 'username', compare username from db with username
    # that is stored in session cookie during login by looking up 'username' only
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
# User account page
# with username as route, preventing visitors without cookie to see this page
@ app.route("/user/<account>", methods=["GET", "POST"])
# and passing username as argument
def user(account):
    # get user profile where user is equal to session user stored during log in
    # but exclude password
    account = mongo.db.users.find_one({"username": session["user"]})
    # {"username": session["user"]}, {"password": 0})
    # test what's stored
    # print(username)
    # print(session["user"])
    # print(session["profile"])
    # if session cookie truthy,
    # then render profile.html with the username information
    if session["user"]:
        return render_template("user.html", account=account)
    # if not truthy, redirect visitor to login page
    return redirect(url_for("login"))
    # from here, we can store the username cookie as menu link in base.html
    # to ensure that only identified users can load their profile


# ------------------------------------------------------------------------------
# User edit account page
# with username as route, preventing visitors without cookie to see this page
@ app.route("/edit_user/<user_id>", methods=["GET", "POST"])
# and passing username as argument
def edit_user(user_id):
    # POST
    if request.method == "POST":
        # using $set to update and not deleted values that are empty
        submit = {"$set": {
            "username": request.form.get("username").lower(),
            "email": request.form.get("email").lower()
        }}
        mongo.db.users.update_one({"_id": ObjectId(user_id)}, submit)
        flash("User Information Successfully Updated, Log In To Use New Info")
        account = mongo.db.users.find_one({"username": session["user"]})
        return render_template("user.html", account=account)

    # GET
    # get user profile where user is equal to session user stored during log in
    user = mongo.db.users.find_one({"username": session["user"]})
    # get user objectid from stored 'user'
    # user_id = user['_id']
    # if 'user' session cookie truthy, render edit_user.html with account info
    if session["user"]:
        return render_template("edit_user.html", user=user)
    # if not truthy, redirect visitor to login page
    return redirect(url_for("login"))


# ------------------------------------------------------------------------------
# User logout
@ app.route("/logout")
def logout():
    # logout message
    flash("You have been logged out")
    # remove 'user' session cookie
    session.pop("user")
    # session.pop("profile")
    # return to login page
    return redirect(url_for("login"))


# ------------------------------------------------------------------------------
# Run Flask application
# Get IP and PORT number and run Flask application in debug mode
if __name__ == "__main__":
    app.run(host=os.environ.get("IP"),
            port=int(os.environ.get("PORT")),
            debug=True)
