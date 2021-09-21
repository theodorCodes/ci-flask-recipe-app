*A full-stack site that allows users to manage a common dataset of recipes, covering the most common database queries such as create, read, update and delete functions.*

**Preview Image of Application Here**

Users can make use of this site to share their recipes with the community and can benefit from having convenient access to the data provided by all other members. This Flask, MongoDB project is part of the Code Institute's milestone project 3.

You can visit the page and play the game right [here!](https://ci-flask-recipe-app.herokuapp.com) 







### Table of Contents

-   [Project](#project)
    -   [Project Introduction](#project-introduction)
    -   [User Story and Goals](#user-story-and-goals)
    -   [Developer Story and Goals](#developer-story-and-goals)
-   [Features](#features)
    -   [Features Implemented](#features-implemented)
    -   [Features Left to Implement](#features-left-to-implement)
-   [Design](#design)
    -   [Database Schema](#database-schema)
    -   [UX Design Choices](#ux-design-choices)
    -   [Wireframes and Layout](#wireframes-and-layout)
-   [Technologies Used](#technologies-used)
-   [Testing](#testing)
    -   [HTML on W3C Validator](#html-on-w3c-validator)
    -   [CSS on W3C Jigsaw Validator](#css-on-w3c-jigsaw-validator)
    -   [JSHint and JavaScript](#jshint-and-javascript)
    -   [Issues and Bug fixes](#issues-and-bug-fixes)
    -   [Performance Test with Lighthouse](#performance-test-with-lighthouse)
-   [Deployment](#deployment)
-   [Attribution and Credits](#attribution-and-credits)





## Project



### Project Introduction

As part of a student project at Code Institute, I chose to write a recipe application to apply and use Flask, MongoDB, HTML, CSS and JavaScript. In addition to these technologies, I have used the Materialized library as well as custom CSS. In this application, users can view recipes from other contributors, search for particular recipes based on keywords, and register an account to post and update their own recipes to share them with the community.



### User Story and Goals

As a user, I expect a recipe page to be information-rich and easy to use, such as finding the right recipe to follow when you need advide to cook a certain kind of dish. Using this application should be intuitive and usable without any instructions, as you do not have the time while cooking. On the other hand, it has to be entertaining or offer at least a pleasant representation of the content while you browse recipes to get inspired by other contributors. Having the possibility to exchange experiences with other members of the community over some dishes and how to get the desired result is important, as you too often try and fail. As a user, I want to share a recipe and get feedback as well. I would like to revise the recipe while I am learning and advancing my cooking skills.



### Developer Story and Goals

**Hands-on experience** of applying and building something with Flask and MongoDB after going through a long process of learning the ins and outs of Python and document based databases. When you see data flowing in your application, applying the CRUD operations and working with data is fun and rewarding. **Implementation of features**, **running tests** and gaining **valuable experience** and problem-solving **practice**.

[back to top](#table-of-contents)





## Features



### Features Implemented

This site consists of a landing page where all recipes are loaded as preview cards. Clicking on the card will lead the visitor to the recipe detail page, where recipe data is presented and structured in cards such as quick info about the meal, cuisine, and diet, as well as preparation time and cooking time, as well as yield, to inform the visitor about some facts about the dish presented. In the same card stack, the user will find the necessary ingredients, kitchen utensils needed, as well as a step-by-step instruction section that users can follow if they wish to cook the presented dish. In addition to this, the recipe detail page has a photo section with a story section attached to it, where users can add their personal story about this dish or recipe. Furthermore, a search bar on both the landing and recipe details pages lets visitors search for recipes.

As a user who is logged in, you can update your profile with information such as your bio and website information if you wish. The user can upload new recipes, revise old ones or delete a recipe.

For site owners the ingredients and utensils section has shopping button which can link to a shopping page. 

[back to top](#table-of-contents)



### Features Left to Implement

Another feature or list of features would be that operators can link a shop to it where you can buy ingredients and cooking utensils needed to cook the presented recipe.

As sharing and communication are an essential and fun part of cooking, this site should have the capability to share, like, and comment on recipes. I have just rendered these features but they are not functional yet, as well as a section of recommendations that shows other dishes or variations of the same to fully emerge in one specific topic.

[back to top](#table-of-contents)





## Design



### Database schema

```bash
# Database schema

recipe_db
   |
   |--- cuisines
   |--- diets
   |--- ingredients
   |--- meals
   |
   |--- recipes
   |
   |--- profiles
   |--- users
   

Main functions planned
   |
   |--- recipes()
   |--- search()
   |
   |--- add_recipe()
   |--- recipe_view()
   |--- edit_recipe()
   |--- delete_recipe()
   |
   |--- user_profile()
   |--- edit_profile()
   |--- user_account()
   |--- edit_account()
   |
   |--- register()
   |--- login()
   |--- logout()

```

[back to top](#table-of-contents)





### UX Design Choices

The navigation throughout this application is designed to be intuitive. To keep the design simple, the base colors are neutral and low-profile, while the recipe cards are designed to spark with their own aura and keep the eye busy and therefore focused on the content.

[back to top](#table-of-contents)



### Wireframes and Layout

The application layout is fairly simple and consist of the navigation bar and the recipe view with preview cards and search function bar while the recipe detail page has a layout of structured cards with quick info about the meal, cuisine, and diet, as well as preparation time and cooking time, as well as yield, to inform the visitor about some facts about the dish presented.

Homepage / recipe overview

**Your image here**



Recipe view

**Your image here**



User profile page 

**Your image here**



Add recipe page

**Your image here**



Edit profile page

**Your image here**



[back to top](#table-of-contents)





## Technologies Used



This project is written in **Python**, using the Flask micro framework with **Jinja** and **HTML**, **CSS** and **JavaScript**. This project is built using the **MongoDB** database and the Atlas service as the DBMS and host of the database. In addition to this stack, the **Materialized** framework is used, as well as some **jQuery**. All of the custom code is written with the **Visual Studio Code** editor on a personal **Mac computer** while the code is hosted on a **Linux** home server during development time. This project uses **Git** for version control and is stored as a public repository on **GitHub**. **Sketch** is used to create the wireframe layout as well as the images in this README file.

[back to top](#table-of-contents)





## Testing



### Python Syntax Checker PEP8

This test has been conducted with the [Python Syntax Checker PEP8](https://www.pythonchecker.com/).

Result: 100%

[back to top](#table-of-contents)





### HTML on W3C Validator

The **HTML** code has not been validated by the W3C validator and it unfortunately is not possible or I have not found the right validator. Proper checking might be problematic as the code written is a fusion of HTML and the Jinja language.

[back to top](#table-of-contents)





### CSS on W3C Jigsaw Validator

The **CSS** code has been validated by direct input in the [W3C Jigsaw validator](https://jigsaw.w3.org/css-validator/) and the respond of the validator has been positive:
Sorry! We found the following errors (1)

.card-subtitle    Property `weights` doesn't exist. The closest matching property name is `height` : 700

Issue is fixed: from `weights` to `font-weight`

[back to top](#table-of-contents)





### JSHint and JavaScript

The **JavaScript** code has been validated by direct input on [JSHint](https://jshint.com/) and resulted in the following message:

**Metrics:** 

There is only one function in this file.
It takes no arguments.
This function contains 3 statements.
Cyclomatic complexity number for this function is 1.

[back to top](#table-of-contents)





### Issues and Bug fixes

These are issues, bugs, and things I struggled with while developing views and functions during the assignment project.



**Issue description: 1**

When trying to store a MongoDB ObjectId () in Flask as a session variable while working on the registration function, I encountered the following error:

```
TypeError
TypeError: Object of type ObjectId is not JSON serializable
```

To solve this issue, I had to first figure out what data type I was actually working with using type ():

```bash
# Things to test, statements that created undesired results or "bugs"
# 1
_id = mongo.db.users.insert_one(register)

# 2
session["user"] = str(_id.inserted_id)

# 3
test = mongo.db.users.find_one({"_id": ObjectId(str(_id.inserted_id))}, {"password": 0})


# Testing using type()
print(type(_id))              # <class 'pymongo.results.InsertOneResult'>
print(type(_id.inserted_id))  # <class 'bson.objectid.ObjectId'>
print(type(session))          # <class 'werkzeug.local.LocalProxy'>
print(session)                # <SecureCookieSession {'user': '613ef67773589829cd3e1d89'}>
print(session["user"])        # 613ef67773589829cd3e1d89

print(test)                   
# {'_id': ObjectId('613ef67773589829cd3e1d89'), 'username': 'test', 'email': 'test@email.com'}

```

After knowing the type, I converted types into strings using str().
Knowing the different types created (testing different data types) helped to solve the issue.



**Issue description: 2**

When using find_one() and no result is found in MongoDB you get this:

```bash
TypeError: 'NoneType' object is not subscriptable
```

Guessing what the issue is, according to Google Search Results:
https://mongodb.tecladocode.com/mongodb_with_python/faq.html
"NoneType" has no attribute and you should add a "return" statement to a find() or find_one() query. So I'm doing this right now...

https://newbedev.com/typeerror-nonetype-object-is-not-subscriptable-flask-python-code-example
This error occurs when you try to use the integer type value as an array. In simple terms, this error occurs when your program has a variable that is treated as an array by your function, but actually, that variable is an integer.
Happens if you append a "None" Value to a list/ array / dictionary


Testing with sort () as well as getting more error messages from mongodb:

```
AttributeError: 'str' object has no attribute 'sort'
AttributeError: 'dict' object has no attribute 'sort'
```

My solution in the end was to do a general document request without specifying ['user']



**Issue description: 3**

werkzeug.exceptions.BadRequestKeyError

https://stackoverflow.com/questions/61831165/getting-werkzeug-exceptions-badrequestkeyerror-400-bad-request-upon-creating

A `BadRequest` error is thrown when you try to access a object or field from the request when the client hasn't sent the field in the request. It seems that you have made typo in you postman request. Also make sure to access it like this`request.form['']`

**Issue solved:** each form needed a submit button and I tried to submit two forms with one submit button.

[back to top](#table-of-contents)





### Performance Test with Lighthouse

**Google Chrome's Developer Tools** are used extensively for debugging as well as the built-in **Lighthouse** project to test the performance of this application. The responsive design has been tested using **Google Chrome's responsive feature** that emulates the screen sizes of various mobile devices.

When the Lighthouse generated a report for the **desktop** view, it produced the following results in the following categories:

-   Performance: 62
-   Accessibility: 97
-   Best Practices: 100
-   SEO: 82

When the Lighthouse generated a report for the **mobile** view, it produced the following results in the following categories:

-   Performance: 34
-   Accessibility: 97
-   Best Practices: 100
-   SEO: 85

The low performance is explained as being due to the non-optimized image size provided.

[back to top](#table-of-contents)





## Deployment

The repository of this project is stored on **GitHub** and the site is deployed at **Heroku**. Please visit the project website by clicking [here!](https://ci-flask-recipe-app.herokuapp.com) 



### Heroku Setup

**Requirements:**

-   requirements.txt
-   Procfile

```bash
# create the needed Procfile
echo web: python app.py > Procfile

# Open Procfile to check out the content
sudo nano Procfile

# Inside Procfile - Content:
web: python app.py


# The Procfile might add a blank line at the bottom, 
# and sometimes this can cause problems when running our app on Heroku, 
# so just delete that line and save the file
```



**Deployment on Heroku, a step by step guide:**

1.   Register/ Login into your Heroku.com account
2.   Click on the "New" button and choose "Create new app" from the dropdown menu
3.   Enter a unique name for your project (such as: ci-flask-recipe-app)
4.   Choose a region
5.   And click "Create app"

**Once your project page is loaded you can connect to your project via GitHub:**

1.   Click on the "Deploy" button in the menu bar
2.   In the "Deployment method" section, choose "GitHub Connect to GitHub"
3.   In the "Connect to GitHub" section, enter your GitHub project name and click the "Search" button
4.   Then click "Connect"
5.   Do not click on the "Deploy Branch" button yet, as we have to setup the environment variables!

**Setting up environment variables for the project:**

1.   Click on the "Settings" button in the menu bar
2.   Go to the "Config Vars" section, and click on the "Reveal Config Vars" button
3.   Then enter your environment variables as you have set in your env.py file
     1.   IP / 0.0.0.0
     2.   PORT / 5000
     3.   SECRET_KEY / <yourrandomkey>
     4.   MONGO_URI / mongodb+srv://root:<yourusername>@myfirstcluster.ltpfu.mongodb.net/recipe_db?retryWrites=true&w=majority
     5.   MONGO_DBNAME / <yourdbname>

**Deploy your project:**

1.   Click on the "Deploy" button in the menu bar
2.   In the "Automatic deploys" section, click on "Enable Automatic Deploys"
3.   In the "Manual deploy" section, choose the GitHub repository branch (by default it's set to master)
4.   Then click on the "Deploy Branch" button
5.   Once Heroku has deployed your project, you will find a little "View" button on the bottom.
6.   Click on the "View" button to see your project in the browser.

**The browser address/url should look like something to this:**

```bash
https://ci-flask-recipe-app.herokuapp.com
```

[back to top](#table-of-contents)





## Attribution and Credits

The [Code Institute](https://codeinstitute.net/) initiated this project to teach and mentor students on their path to becoming software developers.

A huge thank you to the Stack Overflow community in general, where I found a lot of answers to questions I had while working on this project. I had a lot of questions while going through this project and have listed the links below as well as the questions I had during my journey.

How to update hashed password:

https://medium.com/codex/simple-registration-login-system-with-flask-mongodb-and-bootstrap-8872b16ef915

How to get ObjectId right after insert_one() in MongoDB:

https://stackoverflow.com/questions/8783753/how-to-get-the-object-id-in-pymongo-after-an-insert

https://www.w3schools.com/python/python_mongodb_insert.asp

https://www.w3schools.com/python/showpython.asp?filename=demo_mongodb_insert_id

How to create user avatar:

https://blog.miguelgrinberg.com/post/the-flask-mega-tutorial-part-vi-profile-page-and-avatars

How to upload images with Flask:

https://blog.miguelgrinberg.com/post/handling-file-uploads-with-flask

How to save image names without extension

https://www.pythonpool.com/python-get-filename-without-extension/

How to use Jinja to create a dynamic path to store images in file system:

https://stackoverflow.com/questions/19511175/variable-in-flask-static-files-routing-url-forstatic-filename

How to have column order in mobile view:

https://stackoverflow.com/questions/32829567/change-div-order-with-css-depending-on-device-width/32829829

How to create a masonry with flex box:

https://tobiasahlin.com/blog/masonry-with-css/

How to delete images from server with flask:

https://stackoverflow.com/questions/26647248/how-to-delete-files-from-the-server-with-flask

How to delete a specific value from a list in MongoDB:
https://stackoverflow.com/questions/16959099/how-to-remove-array-element-in-mongodb

A big thank you as well to the **Unsplash** community, where I got the images that you see on the site. The dummy text for the recipes on the site is from several different authors, and their names are listed in the recipes when they are available on any given site I have looked up.

[back to top](#table-of-contents)