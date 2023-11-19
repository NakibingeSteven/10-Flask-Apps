from flask import Flask
from flask import render_template
from flask import redirect
from flask import url_for
from flask import flash

from flask_login import LoginManager
from flask_login import UserMixin
from flask_login import login_user
from flask_login import login_required
from flask_login import logout_user
from flask_login import current_user

from flask_wtf import FlaskForm
from wtforms import StringField
from wtforms import PasswordField
from wtforms import SubmitField
from wtforms.validators import DataRequired, Length

from werkzeug.security import generate_password_hash, check_password_hash

# the app
app = Flask(__name__)
app.config["SECRET_KEY"] = "your_secret_key"  # Change this to a random secret key

# Setup Flask-Login
login_manager = LoginManager(app)
login_manager.login_view = "login"


# Sample user model
class User(UserMixin):
    def __init__(self, id, username, password):
        self.id = id
        self.username = username
        self.password = password


# Sample database (replace this with a real database)
users_db = {
    1: User(1, "user1", generate_password_hash("password1")),
    2: User(2, "user2", generate_password_hash("password2")),
}


# Sample registration form
class RegistrationForm(FlaskForm):
    username = StringField(
        "Username", validators=[DataRequired(), Length(min=4, max=20)]
    )
    password = PasswordField("Password", validators=[DataRequired(), Length(min=6)])
    submit = SubmitField("Register")


# Sample login form
class LoginForm(FlaskForm):
    username = StringField(
        "Username", validators=[DataRequired(), Length(min=4, max=20)]
    )
    password = PasswordField("Password", validators=[DataRequired(), Length(min=6)])
    submit = SubmitField("Login")


# Flask-Login user loader
@login_manager.user_loader
def load_user(user_id):
    return users_db.get(int(user_id))


# Routes
@app.route("/")
def home():
    return "Welcome to the Home Page!"


@app.route("/register", methods=["GET", "POST"])
def register():
    form = RegistrationForm()

    if form.validate_on_submit():
        # Check if username is already taken
        if any(user.username == form.username.data for user in users_db.values()):
            flash("Username is already taken. Please choose another.", "danger")
        else:
            # Add user to the database
            user_id = max(users_db.keys()) + 1
            new_user = User(
                user_id, form.username.data, generate_password_hash(form.password.data)
            )
            users_db[user_id] = new_user

            flash("Registration successful. You can now log in.", "success")
            return redirect(url_for("login"))

    return render_template("register.html", form=form)


@app.route("/login", methods=["GET", "POST"])
def login():
    form = LoginForm()

    if form.validate_on_submit():
        # Check if username exists and password is correct
        user = next(
            (user for user in users_db.values() if user.username == form.username.data),
            None,
        )
        if user and check_password_hash(user.password, form.password.data):
            login_user(user)
            flash("Login successful!", "success")
            return redirect(url_for("home"))
        else:
            flash("Invalid username or password. Please try again.", "danger")

    return render_template("login.html", form=form)


@app.route("/logout")
@login_required
def logout():
    logout_user()
    flash("You have been logged out.", "info")
    return redirect(url_for("home"))


if __name__ == "__main__":
    app.run(debug=True)
