from flask import Flask
from flask import render_template
from flask import request

from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, IntegerField

app = Flask(__name__)
app.config["SECRET_KEY"] = "456"  # Set a secret key for CSRF protection


# simple form
class MyForm(FlaskForm):  # Inherits from FlaskForm
    name = StringField("Name")
    age = IntegerField("Age")
    submit = SubmitField("Submit")


@app.route("/", methods=["GET", "POST"])
def index():
    form = MyForm()  # Creates an instance of the MyForm class.

    if form.validate_on_submit():
        # Handle form submission
        name = form.name.data
        age = form.age.data
        return f"Hello, {name}, your age is {age} ! Form submitted successfully."

    return render_template(
        "form.html", form=form
    )  # Renders the 'index.html' template, passing the form object to the template.


if __name__ == "__main__":
    app.run(debug=True)
