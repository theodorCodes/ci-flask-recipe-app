# ----------------------------------------------------------------------pep8-79
# Dependencies
import os
from flask import (
    Flask, flash, render_template, redirect, request, session, url_for
)
from flask_pymongo import PyMongo
from bson.objectid import ObjectId
from werkzeug.security import generate_password_hash, check_password_hash
# For secure file uploads
from werkzeug.utils import secure_filename

# If available, import content from env.py
if os.path.exists("env.py"):
    import env


# Flask instance
app = Flask(__name__)

# DB connection - Save env.py credentials in config of app instance
app.config["MONGO_DBNAME"] = os.environ.get("MONGO_DBNAME")
app.config["MONGO_URI"] = os.environ.get("MONGO_URI")
app.secret_key = os.environ.get("SECRET_KEY")
# Set image path, max. size and limit allowed image formats
app.config['UPLOAD_FOLDER_AVATAR'] = 'static/images/avatars/'
app.config['UPLOAD_FOLDER_RECIPE'] = 'static/images/recipes/'
app.config['MAX_CONTENT_LENGTH'] = 16 * 1024 * 1024
app.config['ALLOWED_EXTENSIONS'] = ['png', 'jpg', 'jpeg', 'gif']

# PyMongo instance, taking 'app' as parameter
mongo = PyMongo(app)


# -----------------------------------------------------------------------------
# Base route, url
@app.route("/")
# -----------------------------------------------------------------------------
# Recipes homepage
@app.route("/recipes")
def recipes():
    # Save queried data in variable 'recipes'
    recipes = list(mongo.db.recipes.find())
    # Render template 'recipes.html',
    # and make 'recipes' data available for template recipes.html
    return render_template("recipes.html", recipes=recipes)


# -----------------------------------------------------------------------------
# Search recipes (Search index required)
@app.route("/search", methods=["GET", "POST"])
def search():
    # Get query request from form
    query = request.form.get("query")
    # Store queried data in recipes
    recipes = list(mongo.db.recipes.find({"$text": {"$search": query}}))
    # Render page with queried data in recipes to recipes.html
    return render_template("recipes.html", recipes=recipes)


# -----------------------------------------------------------------------------
# Recipe view
@app.route("/recipe_view/<recipe_id>")
def recipe_view(recipe_id):

    # Query recipe by id
    recipe = mongo.db.recipes.find_one({"_id": ObjectId(recipe_id)})

    # Get author profile from recipe
    profile = mongo.db.profiles.find_one({"user_id": recipe["author"]})

    # Test: print(recipe["author"])
    # Test: print(profile["avatar"])

    # Render recipe view and pass recipe and profile info to this view
    return render_template("recipe_view.html", recipe=recipe, profile=profile)


# -----------------------------------------------------------------------------
# Recipe delete
@app.route("/delete_recipe/<recipe_id>")
def delete_recipe(recipe_id):
    # Get recipe image name
    filename = mongo.db.recipes.find_one(
        {"_id": ObjectId(recipe_id)})["recipe_image"]

    # Test: print(filename)

    # Delete image from folder using configured path
    os.remove(os.path.join(app.config['UPLOAD_FOLDER_RECIPE'], filename))

    # Remove recipe from profile with $pull
    delete_recipe = {"$pull": {
        "recipes": recipe_id
    }}

    # And update users profile with delete_recipe info
    profile = mongo.db.profiles.update_one(
        {"user_id": session["user"]}, delete_recipe)

    # Remove recipe from database
    mongo.db.recipes.remove({"_id": ObjectId(recipe_id)})
    flash("Your recipe has been deleted")

    # Then prepare up to date data for my_recipe.html view
    # Query profile data where user_id is equal to session cookie stored
    profile = mongo.db.profiles.find_one(
        {"user_id": session["user"]})

    # Query profiles recipe data where author is equal session cookie stored
    # and store as list to loop through in my_recipes.html
    recipes = list(mongo.db.recipes.find({"author": session["user"]}))

    # if session cookie truthy, render my_recipes.html with profile info
    if session["user"]:
        return render_template(
            "my_recipes.html", profile=profile, recipes=recipes)


# -----------------------------------------------------------------------------
# User add recipe - requires recipe_id in the url
@app.route("/recipe_edit/<recipe_id>", methods=["GET", "POST"])
def recipe_edit(recipe_id):
    if request.method == "POST":

        # Prepare recipe content for insert with $set
        recipe_update = {"$set": {
            "title": request.form.get("title"),
            "subtitle": request.form.get("subtitle"),
            "cuisine": request.form.get("cuisine"),
            "diet": request.form.get("diet"),
            "meal": request.form.get("meal"),
            "preptime": request.form.get("preptime"),
            "cooktime": request.form.get("cooktime"),
            "yield": request.form.get("yield"),
            "ingredients": request.form.get("ingredients"),
            "utensils": request.form.get("utensils"),
            "instructions": request.form.get("instructions"),
            "recipe_story": request.form.get("recipe_story"),
        }}

        # First update data in recipes collection without image
        mongo.db.recipes.update_one(
            {"_id": ObjectId(recipe_id)}, recipe_update)

        # Processing the image
        # More comments about image handling in recipe_add() profile_edit()

        # Store image uploaded in recipe_img
        recipe_img = request.files['file']
        # Sanitise filename of the image
        filename = secure_filename(recipe_img.filename)

        # If image in exists
        if recipe_img.filename != "":

            # Split filename and store the 2nd part (.jpg) in file_extension
            file_extension = os.path.splitext(filename)[1].lstrip(".")

            # If file extension is not allowed as defined in allowed extensions
            if file_extension not in app.config["ALLOWED_EXTENSIONS"]:
                flash("Please use file formats such as JPG, Jpeg, PNG or Gif.")
                return redirect(url_for("recipe_view"))

            # If file extension is allowed
            if file_extension in app.config["ALLOWED_EXTENSIONS"]:

                # Create "new" filename with stored recipe id
                filename = str(recipe_id) + "." + file_extension

                # Save image in configured recipe upload folder
                # (Will overwrite the current, if available with the same name)
                recipe_img.save(os.path.join(
                    app.config['UPLOAD_FOLDER_RECIPE'], filename))

                # Prepare recipe_image filename to be uploaded using $set
                # (Will overwrite the current, if available with the same name)
                recipe_image = {"$set": {
                    "recipe_image": filename
                }}

                # Update newly created recipe image name to the same recipe,
                # using the stored recipe_id to find the recipe in MongoDB
                mongo.db.recipes.update_one(
                    {"_id": ObjectId(recipe_id)}, recipe_image)

                # Send success message to user
                flash("Image saved")

        # If image does not exist in post request send user back to recipe_view

        # Flash message to user
        flash("Recipe Added")

        # Prepare profile data for the template
        profile = mongo.db.profiles.find_one(
            {"user_id": session["user"]})

        # Prepare recipe data
        recipe = mongo.db.recipes.find_one({"_id": ObjectId(recipe_id)})

        # Render template with profile and recipe data
        return render_template("recipe_view.html", profile=profile, recipe=recipe)

    # Default template launche with recipe data
    recipe = mongo.db.recipes.find_one({"_id": ObjectId(recipe_id)})

    # Get categories data
    cookingtime = mongo.db.cookingtime.find().sort("cooktime", 1)
    cuisines = mongo.db.cuisines.find().sort("cuisine", 1)
    diets = mongo.db.diets.find().sort("diet", 1)
    ingredients = mongo.db.ingredients.find().sort("ingredient", 1)
    meals = mongo.db.meals.find().sort("meal", 1)

    # Render page with recipe and categories from above
    return render_template(
        "recipe_edit.html", recipe=recipe, cookingtime=cookingtime,
        cuisines=cuisines, diets=diets, ingredients=ingredients, meals=meals)


# -----------------------------------------------------------------------------
# User add recipe
@app.route("/recipe_add", methods=["GET", "POST"])
def recipe_add():
    if request.method == "POST":

        # Prepare recipe content for insert
        recipe = {
            "title": request.form.get("title"),
            "subtitle": request.form.get("subtitle"),
            "cuisine": request.form.get("cuisine"),
            "diet": request.form.get("diet"),
            "meal": request.form.get("meal"),
            "preptime": request.form.get("preptime"),
            "cooktime": request.form.get("cooktime"),
            "yield": request.form.get("yield"),
            "ingredients": request.form.get("ingredients"),
            "utensils": request.form.get("utensils"),
            "instructions": request.form.get("instructions"),
            "recipe_image": "",
            "recipe_story": request.form.get("recipe_story"),
            "likes": [],
            "comments": [],
            "author": session["user"]  # FIX THIS TO PROFILE
        }

        # Insert and retrieve inserted recipe object id at the same time
        recipe_object = mongo.db.recipes.insert_one(recipe)
        # The above stores the given data without the image in MongoDB

        # Test: print(recipe_object.inserted_id)

        # Using MongoDB provided .inserted_id to output created id
        # and converting this recipe object id into a string
        recipe_id = str(recipe_object.inserted_id)

        # Test: print(recipe_id)

        # Processing the image
        # More comments about image handling in profile_edit()

        recipe_img = request.files['file']
        filename = secure_filename(recipe_img.filename)

        # If image in exists
        if recipe_img.filename != "":

            # Split filename and store 2nd part (.jpg) in file_extension
            file_extension = os.path.splitext(filename)[1].lstrip(".")

            # If file extension is not allowed
            if file_extension not in app.config["ALLOWED_EXTENSIONS"]:
                flash("Please use file formats such as JPG, Jpeg, PNG or Gif.")

                # Query and store profile data where user_id
                # is equal to session cookie stored
                profile = mongo.db.profiles.find_one(
                    {"user_id": session["user"]})

                # Load available recipes
                recipes = list(mongo.db.recipes.find(
                    {"author": session["user"]}))

                # If session cookie truthy,
                # render my_recipes.html with profile and recipe info
                if session["user"]:
                    return render_template(
                        "my_recipes.html", profile=profile, recipes=recipes)

                # If not truthy, redirect visitor to login page
                return redirect(url_for("login"))

            # If file extension is allowed
            if file_extension in app.config["ALLOWED_EXTENSIONS"]:

                # Create new filename with recipe object id
                filename = str(recipe_id) + "." + file_extension

                # And save image in existing recipe upload folder
                recipe_img.save(os.path.join(
                    app.config['UPLOAD_FOLDER_RECIPE'], filename))

                # Prepare recipe image to be uploaded using "$set"
                recipe_image = {"$set": {
                    "recipe_image": filename
                }}

                # Update newly created recipe image name to the same recipe,
                # using the stored recipe id to find the recipe in MongoDB
                mongo.db.recipes.update_one(
                    {"_id": ObjectId(recipe_id)}, recipe_image)

                # Send success message to user
                flash("Image saved")

        # If no image uploaded

        # Prepare recipe object id update to profile,
        # using $addToSet to add to existing recipe 'list' if available
        # This somehow works only because I have already created an empty
        # recipe array for the profile at the def register() function
        recipe_added = {"$addToSet": {
            "recipes": recipe_id
        }}

        # Update users profile with object id of added recipe
        profile = mongo.db.profiles.update_one(
            {"user_id": session["user"]}, recipe_added)

        # Flash message to user
        flash("Recipe Saved")

        # Load profile
        profile = mongo.db.profiles.find_one(
            {"user_id": session["user"]})

        # Load available recipes
        recipes = list(mongo.db.recipes.find({"author": session["user"]}))

        # Return user to my_recipe page if session cookie exists
        if session["user"]:
            return render_template(
                "my_recipes.html", profile=profile, recipes=recipes)

        # Or log user out if no session cookie exists
        return redirect(url_for("login"))

    # Default data to get to render this view
    cookingtime = mongo.db.cookingtime.find().sort("cooktime", 1)
    cuisines = mongo.db.cuisines.find().sort("cuisine", 1)
    diets = mongo.db.diets.find().sort("diet", 1)
    ingredients = mongo.db.ingredients.find().sort("ingredient", 1)
    meals = mongo.db.meals.find().sort("meal", 1)

    # Render page with the categories from above
    return render_template(
        "recipe_add.html", cookingtime=cookingtime, cuisines=cuisines,
        diets=diets, ingredients=ingredients, meals=meals)


# -----------------------------------------------------------------------------
# User my_recipes / profile page - requires user id in url
@ app.route("/my_recipes/<account>", methods=["GET", "POST"])
# Passing user id as argument
def my_recipes(account):

    # Query profile data where user id is equal session cookie stored
    profile = mongo.db.profiles.find_one(
        {"user_id": session["user"]})

    # Query profiles recipe data where author is equal session cookie stored
    # and store as list to loop through in my_recipes.html
    recipes = list(mongo.db.recipes.find({"author": session["user"]}))

    # If session cookie truthy, render my_recipes.html with profile info
    if session["user"]:
        return render_template(
            "my_recipes.html", profile=profile, recipes=recipes)

    # If not truthy, redirect visitor to login page
    return redirect(url_for("login"))

    # Account cookie is set required in menu link at base.html file
    # ensuring that only identified users can load their profile


# -----------------------------------------------------------------------------
# User registration page
@ app.route("/register", methods=["GET", "POST"])
def register():
    # Validate if method in register.html is 'POST"
    if request.method == "POST":

        # Prepare account and store email from form input
        # for existing entry in MongoDB
        existing_user = mongo.db.users.find_one(
            {"email": request.form.get("email").lower()})

        # If user already exists show flash message
        if existing_user:
            flash("Email already exists.")
            flash("Login with current email or try another one.")
            flash("(Password recovery service not available yet)")

            # Redirect visitor to the register page
            return redirect(url_for("register"))

        # If user does not exists, create 'register' variable with input values
        # Storing username, email in lowercase and password from form,
        # using werkzeug to generate password hash
        register = {
            "username": request.form.get("username").lower(),
            "email": request.form.get("email").lower(),
            "password": generate_password_hash(request.form.get("password"))
        }

        # Create account
        # Insert variable 'register' in 'users' collection in MongoDB
        # And store created user info in '_id' variable
        _id = mongo.db.users.insert_one(register)

        # Create session cookie with inserted_id, created during insert_one()
        # and convert the bson object into a string value to avoid TypeError
        session["user"] = str(_id.inserted_id)

        # Query and store user data
        user = mongo.db.users.find_one(
            {"_id": ObjectId(session["user"])}, {"password": 0})

        # Create profile
        # With the inserted_id from MongoDB or session cookie created
        # prepare profile for user with user_id for reference
        profile = {
            "avatar": "",
            "username": request.form.get("username").lower(),
            "website": "",
            "bio": "",
            "user_id": session["user"],
            "recipes": [],
            "followers": []
        }

        # And insert profile in to MongoDB profiles collection
        mongo.db.profiles.insert_one(profile)

        # Give success feedback to user
        flash("Registration Successful!")

        # Redirect user to my_recipes page and passing through username
        # from queried user data to use in my_recipe.html
        return redirect(url_for("my_recipes", account=user['username']))

    # Default - Render register.html template for visitors
    return render_template("register.html")


# -----------------------------------------------------------------------------
# User login page
@ app.route("/login", methods=["GET", "POST"])
def login():
    # Validate if method is 'POST'
    if request.method == "POST":

        # Query input email at MongoDB and store user data in 'existing_user'
        existing_user = mongo.db.users.find_one(
            {"email": request.form.get("email").lower()})

        # If queried user found on MongoDB
        if existing_user:

            # Check hashed password using werkzeug, comparing both
            # the hashed password stored on DB and the password from input
            if check_password_hash(
                    existing_user["password"], request.form.get("password")):

                # Create session cookie for user with user id as string type
                session["user"] = str(existing_user["_id"])

                # Show message with user stored username (string interpolation)
                flash("Hi {}, Welcome back to Daily Delights".format(
                    existing_user["username"].lower()))

                # And redirect user to my_recipes page
                return redirect(url_for("my_recipes", account=session["user"]))

            # If the password is invalid
            else:
                # Show this message to visitor
                flash("Your Email and/or Password does not match")
                # and redirect visitor back to the login page
                return redirect(url_for("login"))

        # If the user does not exist
        else:
            # Show the same message to visitor
            flash("Your Email and/or Password does not match")
            # and redirect visitor back to the login page
            return redirect(url_for("login"))

    # Default - Render login.html template for visitors
    return render_template("login.html")


# -----------------------------------------------------------------------------
# User profile edit page
@ app.route("/profile_edit/<account>", methods=["GET", "POST"])
def profile_edit(account):
    # Validate if method is 'POST'
    if request.method == "POST":

        # PROCESSING IMAGE CONTENT
        # Credits to Miguel Grinberg and his tutorial on how to save images
        # https://blog.miguelgrinberg.com/post/handling-file-uploads-with-flask

        # Store file from input in variable avatar_file
        avatar_file = request.files['file']

        # Store filename in filename with Werkzeug secure_filename() method
        # This step might be not necessary as I will rename the file below
        filename = secure_filename(avatar_file.filename)

        # If image request is not empy then process the image file
        if avatar_file.filename != "":

            # Validating filename extension
            # Extract file extension name with os.path.splitext() method
            # using [1] seperates the filename before the dot resulting in .jpg
            # outputting the second part of the splitted content, the content
            # .jpg has a dot, using str.lstrip(".") to delete the dot
            file_extension = os.path.splitext(filename)[1].lstrip(".")

            # Test: print(file_extension) # outputs jpg instead dot .jpg

            # If extension is none in the allowed list defined
            if file_extension not in app.config["ALLOWED_EXTENSIONS"]:

                # Show flash message
                flash(
                    "Please use file formats such as JPG, Jpeg, PNG or Gif.")

                # And refresh the page getting account data
                account = mongo.db.users.find_one(
                    {"_id": ObjectId(session["user"])})["_id"]

                # Get profile data
                profile = mongo.db.profiles.find_one(
                    {"user_id": session["user"]})

                # And render the page with account and profile data
                if session["user"]:
                    return render_template("profile_edit.html",
                                           account=account, profile=profile)

            # If the extension is one of the allowed extensions
            if file_extension in app.config["ALLOWED_EXTENSIONS"]:

                # Re-assign custom filename using "users id" and extension name,
                # using the user id as image reference to the profile
                filename = session['user'] + "." + file_extension

                # Test: print(filename)

                # Then save file using os.path.join()
                # and the pre-defined image path app.config['UPLOAD_FOLDER_AVATAR']
                # and the new custom filename which is the user id
                # (This will overwrite anything stored with the same name
                # except if the extension is not the same)
                avatar_file.save(os.path.join(
                    app.config['UPLOAD_FOLDER_AVATAR'], filename))

                # Show flash success message to user
                flash("Avatar saved")

        # PROCESSING TEXT CONTENT
        # Include the avatar filename from above if available in the submission
        # if the first part of splitted filename without the extension .jpg
        # is equal to the current user
        avatar_img = filename.rpartition('.')[0]

        # print("avatar test: " + avatar_img)

        # Checking again if logged in user is equal to avatar image name
        if avatar_img == session["user"]:

            # Using $set to not overwrite document with empty content
            submit = {"$set": {
                "avatar": filename,
                "website": request.form.get("website"),
                "bio": request.form.get("bio")
            }}

        # If filename is not available then prepare the submission like below
        else:
            # Test: print("no avatar updates")
            submit = {"$set": {
                "website": request.form.get("website"),
                "bio": request.form.get("bio")
            }}

        # Submit input-data in profiles collection where user_id equals
        # the session cookie stored during registration or login
        mongo.db.profiles.update_one({"user_id": session["user"]}, submit)

        # Show success message to user
        flash("Profile Successfully Updated")

        # Query account id
        account = mongo.db.users.find_one(
            {"_id": ObjectId(session["user"])})["_id"]

        # Test: print("Account info: " + str(account))

        # Query the updated profile data and store in 'profile'
        profile = mongo.db.profiles.find_one(
            {"user_id": session["user"]})

        # Query recipes available
        recipes = list(mongo.db.recipes.find({"author": session["user"]}))

        # Then return to my_repices.html
        # and render the page with updated profile data
        if session["user"]:
            return render_template(
                "my_recipes.html", account=account,
                profile=profile, recipes=recipes)

    # Store user data where object id is equal to session cookie
    # stored during log in but exclude password
    account = mongo.db.users.find_one(
        {"_id": ObjectId(session["user"])}, {"password": 0})

    # Store profile data where user_id is equal to session user

    # test: print(session["user"])

    profile = mongo.db.profiles.find_one(
        {"user_id": session["user"]})

    # test: print(profile)

    # If 'user' session cookie truthy, render edit_user.html
    # and passing account and profile data
    if session["user"]:
        return render_template("profile_edit.html",
                               account=account, profile=profile)

    # If not truthy, redirect visitor to login page
    return redirect(url_for("login"))


# -----------------------------------------------------------------------------
# User account page - Requires account id in url
@ app.route("/user/<account>")
# Passing username as argument
def user(account):

    # Get user data where object id is equal to session cookie stored during
    # log in but exclude password
    account = mongo.db.users.find_one(
        {"_id": ObjectId(session["user"])}, {"password": 0})

    # If session cookie truthy,
    # then render user.html with username information
    if session["user"]:
        return render_template("user.html", account=account)

    # If not truthy, redirect visitor to login page
    return redirect(url_for("login"))

    # Account cookie is set required in menu link at base.html file
    # to ensure that only identified users can load their profile


# -----------------------------------------------------------------------------
# User account edit page - Requires user in in url
@ app.route("/user_edit/<user_id>", methods=["GET", "POST"])
# Passing user id as argument
def user_edit(user_id):

    # Validate if method is 'POST'
    if request.method == "POST":

        # Store email request in email_requested
        email_requested = request.form.get("email").lower()

        # Test: print(email_requested)

        # Check resquest email in MongoDB for existing accounts
        # Tested if no account found with this email the output is 'None'
        existing_email = mongo.db.users.find_one(
            {"email": request.form.get("email").lower()})

        # Test: print(existing_email)

        # Store current user email where object id is equal to session cookie
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

    # Default - Get user data where user is equal to session user
    user = mongo.db.users.find_one(
        {"_id": ObjectId(session["user"])}, {"password": 0})

    # If 'user' session cookie truthy, render edit_user.html with account info
    if session["user"]:
        return render_template("user_edit.html", user=user)

    # If not truthy, redirect visitor to login page
    return redirect(url_for("login"))


# -----------------------------------------------------------------------------
# User logout
@ app.route("/logout")
def logout():
    # Logout message
    flash("You have been logged out")

    # Remove 'user' session cookie
    session.pop("user")

    # Return to login page
    return redirect(url_for("login"))


# -----------------------------------------------------------------------------
# Run Flask application
# Get IP and PORT number and run Flask application in debug mode
if __name__ == "__main__":
    app.run(host=os.environ.get("IP"),
            port=int(os.environ.get("PORT")),
            debug=False)
