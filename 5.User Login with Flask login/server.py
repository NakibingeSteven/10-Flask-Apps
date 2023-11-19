from flask import Flask, render_template, redirect, url_for, request
from flask_login import (
    LoginManager,
    UserMixin,
    login_user,
    login_required,
    logout_user,
    current_user,
)
from werkzeug.security import generate_password_hash, check_password_hash

app = Flask(__name__)
app.config["SECRET_KEY"] = "mysecretkey"
login_manager = LoginManager(app)


class User(UserMixin):
    def __init__(self, user_id, username, email, password, age, sex, address):
        self.id = user_id
        self.username = username
        self.email = email
        self.password = generate_password_hash(password)
        self.age = age
        self.sex = sex
        self.address = address


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


@login_manager.user_loader
def load_user(user_id):
    return users.get(user_id)


@app.route("/")
def home():
    return "<h1>This is the Home Page</h1>"


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


@app.route("/register", methods=["GET", "POST"])
def register():
    if request.method == "POST":
        # getting the values from the form
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

    # render teh template
    return render_template("register.html")


if __name__ == "__main__":
    app.run(debug=True)
