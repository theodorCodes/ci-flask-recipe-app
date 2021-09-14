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
        # get email from mongodb and validate with email from form input
        existing_user = mongo.db.users.find_one(
            {"email": request.form.get("email").lower()})
        # if user already exists show flash message
        if existing_user:
            flash("Email already exists.")
            flash("Login with current email or try another one.")
            flash("(Password recovery service not available yet)")
            # redirect visitor to the register page
            return redirect(url_for("register"))
        # if user does not exists, create variable 'register' with input values
        register = {
            # store username, email in lowercase
            "username": request.form.get("username").lower(),
            "email": request.form.get("email").lower(),
            # and password from form, using werkzeug to generate password salt
            "password": generate_password_hash(request.form.get("password"))
        }
        # insert variable 'register' in 'users' collection on mongodb
        # AND store created user-info in '_id' variable
        _id = mongo.db.users.insert_one(register)
        # create session cookie with inserted_id, created during insert_one()
        # and convert the bson object into a string value
        session["user"] = str(_id.inserted_id)
        # query and store user data
        user = mongo.db.users.find_one(
            {"_id": ObjectId(session["user"])}, {"password": 0})
        # give success feedback to user
        flash("Registration Successful!")
        # redirect user to my_recipes page and passing through username
        # from queried user data to use in my_recipe.html
        return redirect(url_for("my_recipes", account=user['username']))

    # default - render register.html template for visitors
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
                # create session cookie for user with user id as string
                session["user"] = str(existing_user["_id"])
                # send message with user stored username
                flash("Hi {}, Welcome back to Daily Delights".format(
                    existing_user["username"].lower()))
                # and redirect user to my_recipes page
                return redirect(url_for("my_recipes", account=session["user"]))
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

    # default - render login.html template for visitors
    return render_template("login.html")


# ------------------------------------------------------------------------------
# User my_recipes, profile page
# with user id in route, preventing visitors without cookie to see this page
@ app.route("/my_recipes/<account>", methods=["GET", "POST"])
# and passing user id here as argument
def my_recipes(account):
    # in variable 'account', compare ObjectId from db with user id
    # stored in session cookie during registration or login
    account = mongo.db.users.find_one(
        {"_id": ObjectId(session["user"])}, {"password": 0})
    # if session cookie truthy,
    # then render my_recipes.html with the user information
    if session["user"]:
        return render_template("my_recipes.html", account=account)
    # if not truthy, redirect visitor to login page
    return redirect(url_for("login"))
    # account cookie is set required in menu link at base.html file
    # ensuring that only identified users can load their profile


# ------------------------------------------------------------------------------
# User profile page
@ app.route("/profile/<account>")
def profile(account):
    # get profile data
    profile = mongo.db.profiles.find_one(
        {"user_id": session["user"]})
    # if 'user' session cookie truthy, render profile.html with profile info
    if session["user"]:
        return render_template("profile.html", profile=profile)
    # if not truthy, redirect visitor to login page
    return redirect(url_for("login"))


# ------------------------------------------------------------------------------
# User profile page
@ app.route("/profile_edit/<account>", methods=["GET", "POST"])
def profile_edit(account):
    # submit button actions
    # validate if method is 'POST'
    if request.method == "POST":
        submit = {"$set": {
            "website": request.form.get("website"),
            "bio": request.form.get("bio")
        }}
        mongo.db.profiles.update({"user_id": session["user"]}, submit)
        flash("Profile Successfully Updated")
        profile = mongo.db.profiles.find_one(
            {"user_id": session["user"]})
        return render_template("profile.html", profile=profile)
    # get user data where object id is equal to session cookie stored during
    # log in but exclude password
    account = mongo.db.users.find_one(
        {"_id": ObjectId(session["user"])}, {"password": 0})
    # get profile data where user_id is equal to session user stored during log in
    # test: print(session["user"])
    profile = mongo.db.profiles.find_one(
        {"user_id": session["user"]})
    # test: print(profile)
    # if 'user' session cookie truthy, render edit_user.html with account info
    if session["user"]:
        return render_template("profile_edit.html", account=account, profile=profile)
    # if not truthy, redirect visitor to login page
    return redirect(url_for("login"))


# ------------------------------------------------------------------------------
# User account page
# with user id in route, preventing visitors without cookie to see this page
@ app.route("/user/<account>")
# and passing username as argument
def user(account):
    # get user data where object id is equal to session cookie stored during
    # log in but exclude password
    account = mongo.db.users.find_one(
        {"_id": ObjectId(session["user"])}, {"password": 0})
    # if session cookie truthy,
    # then render user.html with username information
    if session["user"]:
        return render_template("user.html", account=account)
    # if not truthy, redirect visitor to login page
    return redirect(url_for("login"))
    # account cookie is set required in menu link at base.html file
    # to ensure that only identified users can load their profile


# ------------------------------------------------------------------------------
# User account edit page
# with user id in route, preventing visitors without cookie to see this page
@ app.route("/user_edit/<user_id>", methods=["GET", "POST"])
# and passing user id as argument
def user_edit(user_id):
    # submit button actions
    # validate if method is 'POST'
    if request.method == "POST":
        # store email request
        email_requested = request.form.get("email").lower()
        # test: print(email_requested)
        # check resquest email in mongodb for existing accounts
        # tested: if no account found with this email the result is 'None'
        existing_email = mongo.db.users.find_one(
            {"email": request.form.get("email").lower()})
        # test: print(existing_email)
        # store current user email
        current_user_email = mongo.db.users.find_one(
            {"_id": ObjectId(session["user"])})["email"]
        # test: print(current_user_email)
        # store passwords from user input
        password = request.form.get("password")
        password2 = request.form.get("password2")
        # if email_requested is not equal to current_user_email and no
        # existing user with this email found or email request and current email is the same
        if email_requested != current_user_email and existing_email == None or email_requested == current_user_email:
            # test: print("email ok to use")
            # check if password not empty and if both password match
            if password != "" and password != password2:
                flash("Passwords do not match")
            # check if password not empty and if both password match
            elif password != "" and password == password2:
                submit = {"$set": {
                    "username": request.form.get("username").lower(),
                    "email": request.form.get("email").lower(),
                    "password": generate_password_hash(request.form.get("password"))
                }}
                # test: print("full update prepared")
                # update in mongodb where user id matches the user id
                mongo.db.users.update_one({"_id": ObjectId(user_id)}, submit)
                # give success feedback to user
                flash("Update Successful. Log in with your new credentials!")
                # get update user data from mongodb
                account = mongo.db.users.find_one(
                    {"_id": ObjectId(session["user"])}, {"password": 0})
                return render_template("user.html", account=account)
            else:
                submit = {"$set": {
                    "username": request.form.get("username").lower(),
                    "email": request.form.get("email").lower(),
                }}
                # test: print("partial update prepared")
                mongo.db.users.update_one({"_id": ObjectId(user_id)}, submit)
                flash("Update Successful")
                account = mongo.db.users.find_one(
                    {"_id": ObjectId(session["user"])}, {"password": 0})
                return render_template("user.html", account=account)

    # get user data where user is equal to session user stored during log in
    user = mongo.db.users.find_one(
        {"_id": ObjectId(session["user"])}, {"password": 0})
    # if 'user' session cookie truthy, render edit_user.html with account info
    if session["user"]:
        return render_template("user_edit.html", user=user)
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
