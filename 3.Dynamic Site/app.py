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

# Additional dynamic content
additional_data = {
    "text_content": "This is some dynamic text content.",
    "number_of_items": len(items),
}


# Sample dictionary
sample_dict = {"key1": "value1", "key2": "value2", "key3": "value3"}

# Sample list of dictionaries
list_of_dicts = [
    {"name": "John", "age": 30},
    {"name": "Jane", "age": 25},
    {"name": "Bob", "age": 35},
]


@app.route("/")
def home():
    # Pass all dynamic data to the template
    return render_template(
        "home.html",
        items=items,
        images=images,
        additional_data=additional_data,
        sample_dict=sample_dict,
        list_of_dicts=list_of_dicts,
    )


@app.route("/about")
def about():
    return render_template("about.html")


@app.route("/contact")
def contact():
    return render_template("contact.html")


if __name__ == "__main":
    app.run(debug=True)
