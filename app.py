# ----------------------------------------------------------------------pep8-79
# Dependencies
import os
from flask import (
    Flask, flash, render_template, redirect, request, session, url_for
)
from flask_pymongo import PyMongo
from bson.objectid import ObjectId
from werkzeug.security import generate_password_hash, check_password_hash
# for secure image/file uploads
from werkzeug.utils import secure_filename

# if available, import content from env.py file
if os.path.exists("env.py"):
    import env

# Image upload path and allowed image formats
UPLOAD_FOLDER = 'static/images/avatars/'
ALLOWED_EXTENSIONS = set(['png', 'jpg', 'jpeg', 'gif'])

# Flask instance
app = Flask(__name__)

# DB connection - Save env.py credentials in config of app instance
app.config["MONGO_DBNAME"] = os.environ.get("MONGO_DBNAME")
app.config["MONGO_URI"] = os.environ.get("MONGO_URI")
app.secret_key = os.environ.get("SECRET_KEY")
# Set image configuration and image size limits
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
app.config['MAX_CONTENT_LENGTH'] = 16 * 1024 * 1024

# PyMongo instance, taking 'app' as parameter
mongo = PyMongo(app)


# -----------------------------------------------------------------------------
# Base route, url
@app.route("/")
# -----------------------------------------------------------------------------
# Recipes homepage - get recipes by various categories
@app.route("/recipes")
def recipes():
    # Save queried data in variable 'recipes'
    recipes = mongo.db.recipes.find()
    # Render template 'recipes.html',
    # and make 'recipes' data available for template
    return render_template("recipes.html", recipes=recipes)


# -----------------------------------------------------------------------------
# Meals page - get recipes ordered by meals
@app.route("/meals")
def meals():
    return render_template("meals.html")


# -----------------------------------------------------------------------------
# Cuisine page - get recipes ordered by cuisines
@app.route("/cuisines")
def cuisines():
    return render_template("cuisines.html")


# -----------------------------------------------------------------------------
# Ingredient page - get recipes ordered by ingredients
@app.route("/ingredients")
def ingredients():
    return render_template("ingredients.html")


# -----------------------------------------------------------------------------
# Diets page - get recipes ordered by diets
@app.route("/diets")
def diets():
    return render_template("diets.html")


# -----------------------------------------------------------------------------
# Recipe details page


# -----------------------------------------------------------------------------
# User registration page
@ app.route("/register", methods=["GET", "POST"])
def register():
    # validate if method in register.html is 'POST"
    if request.method == "POST":
        # prepare account
        # query, store email from form input for existing entry in mongodb
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
            # and password from form, using werkzeug to generate password hash
            "password": generate_password_hash(request.form.get("password"))
        }

        # create account
        # insert variable 'register' in 'users' collection on mongodb
        # AND store created user-info in '_id' variable
        _id = mongo.db.users.insert_one(register)
        # create session cookie with inserted_id, created during insert_one()
        # and convert the bson object into a string value to avoid TypeError
        session["user"] = str(_id.inserted_id)
        # query and store user data
        user = mongo.db.users.find_one(
            {"_id": ObjectId(session["user"])}, {"password": 0})

        # create profile
        # with the inserted_id from mongodb or session cookie created
        # prepare profile for user with user_id for reference
        profile = {
            "username": request.form.get("username").lower(),
            "website": "",
            "bio": "",
            "user_id": session["user"]
        }
        # and insert profile in to mongodb profiles collection
        mongo.db.profiles.insert_one(profile)

        # give success feedback to user
        flash("Registration Successful!")
        # redirect user to my_recipes page and passing through username
        # from queried user data to use in my_recipe.html
        return redirect(url_for("my_recipes", account=user['username']))

    # default - render register.html template for visitors
    return render_template("register.html")


# -----------------------------------------------------------------------------
# User login page
@ app.route("/login", methods=["GET", "POST"])
def login():
    # validate if method is 'POST'
    if request.method == "POST":
        # query input email at mongodb and store user data in 'existing_user'
        existing_user = mongo.db.users.find_one(
            {"email": request.form.get("email").lower()})
        # if queried user found on mongodb
        if existing_user:
            # check hashed password using werkzeug, comparing both
            # the hashed password stored on db and the password from input
            if check_password_hash(
                    existing_user["password"], request.form.get("password")):
                # create session cookie for user with user id as string type
                session["user"] = str(existing_user["_id"])
                # show message with user stored username (string interpolation)
                flash("Hi {}, Welcome back to Daily Delights".format(
                    existing_user["username"].lower()))
                # and redirect user to my_recipes page
                return redirect(url_for("my_recipes", account=session["user"]))
            # if the password is invalid
            else:
                # show this message to visitor
                flash("Your Email and/or Password does not match")
                # and redirect visitor back to the login page
                return redirect(url_for("login"))
        # if the user does not exist
        else:
            # show the same message to visitor
            flash("Your Email and/or Password does not match")
            # and redirect visitor back to the login page
            return redirect(url_for("login"))

    # default - render login.html template for visitors
    return render_template("login.html")


# -----------------------------------------------------------------------------
# User my_recipes, profile page
# with user id in route, preventing visitors without cookie to see this page
@ app.route("/my_recipes/<account>", methods=["GET", "POST"])
# and passing user id here as argument
def my_recipes(account):
    # query, store profile data where user_id is equal session cookie stored
    profile = mongo.db.profiles.find_one(
        {"user_id": session["user"]})
    # if session cookie truthy,
    # then render my_recipes.html with profile information
    if session["user"]:
        return render_template("my_recipes.html", profile=profile)
    # if not truthy, redirect visitor to login page
    return redirect(url_for("login"))
    # account cookie is set required in menu link at base.html file
    # ensuring that only identified users can load their profile


# -----------------------------------------------------------------------------
# User profile edit page
@ app.route("/profile_edit/<account>", methods=["GET", "POST"])
def profile_edit(account):
    # validate if method is 'POST'
    if request.method == "POST":

        submit = {"$set": {
            "website": request.form.get("website"),
            "bio": request.form.get("bio")
        }}
        # submit/update input-data in mongodb profiles where user_id equals
        # the session cookie stored during registration or login
        mongo.db.profiles.update({"user_id": session["user"]}, submit)
        # show success message to user
        flash("Profile Successfully Updated")
        # query the updated data just stored in profiles
        profile = mongo.db.profiles.find_one(
            {"user_id": session["user"]})
        # and render the page with newly stored/updated data
        return render_template("my_recipes.html", profile=profile)
        # return render_template("profile.html", profile=profile)

        # avatar logic
        # avatar should be saved

    # query/store user-data where ObjectId is equal to session cookie
    # stored during log in but exclude password
    account = mongo.db.users.find_one(
        {"_id": ObjectId(session["user"])}, {"password": 0})
    # query/store profile-data where user_id is equal to session user
    # test: print(session["user"])
    profile = mongo.db.profiles.find_one(
        {"user_id": session["user"]})
    # test: print(profile)
    # if 'user' session cookie truthy, render edit_user.html
    # passing account and profile data
    if session["user"]:
        return render_template("profile_edit.html",
                               account=account, profile=profile)
    # if not truthy, redirect visitor to login page
    return redirect(url_for("login"))


# -----------------------------------------------------------------------------
# Upload, save avatar
@app.route("/upload_avatar/<account>", methods=['POST', 'GET'])
def upload_avatar(account):
    if request.method == 'POST':
        avatar_file = request.files['file']
        if avatar_file.filename != "":
            avatar_file.save(secure_filename(avatar_file.filename))
            flash("File saved successfully")
        return redirect("profile_edit")

    # if 'user' session cookie truthy, render edit_user.html
    # passing account and profile data
    if session["user"]:
        return render_template("upload_avatar.html", account=account)
    # if not truthy, redirect visitor to login page
    return redirect(url_for("login"))


# -----------------------------------------------------------------------------
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


# -----------------------------------------------------------------------------
# User account edit page
# Using user_id in route to prevent visitors without cookie to see this page
@ app.route("/user_edit/<user_id>", methods=["GET", "POST"])
# and passing user id as argument here
def user_edit(user_id):
    # Submit button actions:
    # Validate if method is 'POST'
    if request.method == "POST":
        # Store email request in email_requested
        email_requested = request.form.get("email").lower()
        # Test: print(email_requested)
        # Check resquest email in mongodb for existing accounts
        # Tested: If no account found with this email the output is 'None'
        existing_email = mongo.db.users.find_one(
            {"email": request.form.get("email").lower()})
        # Test: print(existing_email)
        # Store current user email where ObjectId is equal to session cookie
        current_user_email = mongo.db.users.find_one(
            {"_id": ObjectId(session["user"])})["email"]
        # Test: print(current_user_email)
        # Store passwords from user input
        password = request.form.get("password")
        password2 = request.form.get("password2")
        # If email_requested is not equal to current_user_email
        # and no existing user with this email found
        # or email request and current email is the same
        if email_requested != current_user_email and existing_email == None \
                or email_requested == current_user_email:
            # Test: print("email ok to use")
            # Check if password is not empty and if passwords are different
            if password != "" and password != password2:
                flash("Passwords do not match")
            # Check if password is not empty and if passwords are the same
            elif password != "" and password == password2:
                # Store things to submit in 'submit' with new password
                submit = {"$set": {
                    "username": request.form.get("username").lower(),
                    "email": request.form.get("email").lower(),
                    "password": generate_password_hash(
                        request.form.get("password"))
                }}
                # Test: print("full update prepared")
                # Update, submit to mongodb for this user_id
                mongo.db.users.update_one({"_id": ObjectId(user_id)}, submit)
                # Give success feedback to user
                flash("Update Successful. Log in with your new credentials!")
                # Get, store updated user data from mongodb where user
                # ObjectId is equal to the session cookie
                account = mongo.db.users.find_one(
                    {"_id": ObjectId(session["user"])}, {"password": 0})
                # Redirect to user.html page with updated data
                return render_template("user.html", account=account)
            else:
                # Store things to submit in 'submit' without password
                submit = {"$set": {
                    "username": request.form.get("username").lower(),
                    "email": request.form.get("email").lower(),
                }}
                # Test: print("partial update prepared")
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


# -----------------------------------------------------------------------------
# User logout
@ app.route("/logout")
def logout():
    # logout message
    flash("You have been logged out")
    # remove 'user' session cookie
    session.pop("user")
    # return to login page
    return redirect(url_for("login"))


# -----------------------------------------------------------------------------
# Run Flask application
# Get IP and PORT number and run Flask application in debug mode
if __name__ == "__main__":
    app.run(host=os.environ.get("IP"),
            port=int(os.environ.get("PORT")),
            debug=True)
