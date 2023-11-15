from flask import Flask
from flask import render_template

app = Flask(__name__)

# Sample list of items
items = ["Item 1", "Item 2", "Item 3", "Item 4", "Item 5"]

# Sample list of image URLs
images = [
    "https://example.com/image1.jpg",
    "https://example.com/image2.jpg",
    "https://example.com/image3.jpg",
    "https://example.com/image4.jpg",
    "https://example.com/image5.jpg",
]


@app.route("/")
def home():
    return render_template("home.html", items=items)


@app.route("/about")
def about():
    return render_template("about.html")


@app.route("/contact")
def contact():
    return render_template("contact.html")


if __name__ == "__main":
    app.run(debug=True)
