#app.py

#Starts the website

from flask import Flask, render_template

from search_routes import search_routes


app = Flask(__name__)

app.register_blueprint(search_routes)


@app.route("/")
def home():
    return render_template("index.html")


@app.route("/health")
def health():
    return {
        "message": "Welcome to GunplaDB!",
        "status": "Backend is running."
    }


if __name__ == "__main__":
    app.run(debug=True)
