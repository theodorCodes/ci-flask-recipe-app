import os
from flask import Flask
# import content from env.py file if available
if os.path.exists("env.py"):
    import env


# Flask instance
app = Flask(__name__)


# Create base directory
@app.route("/")
def hello():
    return "Hello World!"


# Get IP and PORT number and run Flask application in debug mode
if __name__ == "__main__":
    app.run(host=os.environ.get("IP"),
            port=int(os.environ.get("PORT")),
            debug=True)
