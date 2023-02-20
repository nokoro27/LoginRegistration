from flask import render_template, redirect, request, session
from flask_bcrypt import Bcrypt
from flask_app import app
from flask_app.models.user import User

bcrypt = Bcrypt(app)


@app.route("/")
def index():
    return render_template("index.html")


@app.route("/register", methods = ["POST"])
def register():
    if not User.register_validator(request.form):
        return redirect("/")


    hash_browns = bcrypt.generate_password_hash(request.form["password"])
    data = {
        **request.form,
        "password": hash_browns
    }

    user_id = User.create(data)

    session["uuid"] = user_id

    return redirect("/dashboard")


@app.route("/login", methods = ["POST"])
def login():
    if not User.login_validator(request.form):

        return redirect("/")

    user = User.get_by_email({"email": request.form["email"]})

    session["uuid"] = user.id

    return redirect("/dashboard")


@app.route("/logout")
def logout():
    session.clear()

    return redirect("/")


@app.route("/dashboard")
def dashboard():
    return render_template("dashboard.html", user = User.get_by_id({"id": session["uuid"]}))