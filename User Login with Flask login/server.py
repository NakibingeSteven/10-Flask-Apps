from flask import Flask, render_template, redirect, url_for, request
from flask_login import (
    LoginManager,
    UserMixin,
    login_user,
    login_required,
    logout_user,
    current_user,
)
from werkzeug.security import check_password_hash

app = Flask(__name__)
app.config["SECRET_KEY"] = "mysecretkey"  # Set a secret key for session management
login_manager = LoginManager(app)  # LoginManager is initialized with the Flask app

# login_view attribute is set to the endpoint ('login') where the user should be redirected
# if they are not logged in and try to access a protected resource.
login_manager.login_view = "login"


# Mock user class (replace this with your User model and database logic)
class User(UserMixin):
    def __init__(self, user_id, username, email, password, age, sex, address):
        self.id = user_id
        self.username = username
        self.email = email
        self.password = (
            password  # In a real application, store hashed passwords, not plain text.
        )
        self.age = age
        self.sex = sex
        self.address = address


# Mock user database (replace this with your database logic)
users = {
    "1": User(
        "1",
        "john_doe",
        "john@example.com",
        "hashed_password",
        25,
        "male",
        "123 Main St",
    ),
    "2": User(
        "2",
        "jane_smith",
        "jane@example.com",
        "hashed_password",
        30,
        "female",
        "456 Oak Ave",
    ),
    # Add more users as needed
}


# this loads a user
@login_manager.user_loader
def load_user(user_id):
    return users.get(user_id)


@app.route("/")
def home():
    return "<h1>This is the Home Page<?h1>"


@app.route("/login", methods=["GET", "POST"])
def login():
    if request.method == "POST":
        username = request.form["username"]
        password = request.form["password"]
        user = next(
            (user for user in users.values() if user.username == username), None
        )
        if user and check_password_hash(user.password, password):
            login_user(user)
            return redirect(url_for("dashboard"))

    return render_template("login.html")


@app.route("/register", methods=["GET", "POST"])
def register():
    if request.method == "POST":
        username = request.form["username"]
        email = request.form["email"]
        password = request.form["password"]
        age = request.form["age"]
        sex = request.form["sex"]
        address = request.form["address"]

        # Check if the username is already taken
        if any(user.username == username for user in users.values()):
            return "Username is already taken. Choose a different username."

        # Create a new user and add it to the user database
        user_id = str(len(users) + 1)
        new_user = User(user_id, username, email, password, age, sex, address)
        users[user_id] = new_user

        # Log in the new user
        login_user(new_user)

        return redirect(url_for("dashboard"))
    return render_template("register.html")


# protected using login_required
@app.route("/dashboard")
@login_required
def dashboard():
    return (
        f'Hello, {current_user.id}! This is the dashboard. <a href="/logout">Logout</a>'
    )


@app.route("/logout")
@login_required
def logout():
    logout_user()
    return redirect(url_for("home"))


if __name__ == "__main__":
    app.run(debug=True)
