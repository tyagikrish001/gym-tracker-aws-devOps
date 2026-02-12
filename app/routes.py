from flask import Blueprint, render_template_string, request, redirect, url_for
from flask_login import login_user, login_required, logout_user, current_user
from .models import User, Workout
from . import db

main = Blueprint('main', __name__)


@main.route("/")
def home():
    return "Gym Tracker App is Live"


@main.route("/register", methods=["GET", "POST"])
def register():
    if request.method == "POST":
        username = request.form.get("username")
        password = request.form.get("password")

        existing_user = User.query.filter_by(username=username).first()
        if existing_user:
            return "User already exists"

        user = User(username=username)
        user.set_password(password)

        db.session.add(user)
        db.session.commit()

        return redirect(url_for("main.login"))

    return render_template_string("""
        <h2>Register</h2>
        <form method="POST">
            Username: <input name="username"><br>
            Password: <input name="password" type="password"><br>
            <button type="submit">Register</button>
        </form>
    """)


@main.route("/login", methods=["GET", "POST"])
def login():
    if request.method == "POST":
        username = request.form.get("username")
        password = request.form.get("password")

        user = User.query.filter_by(username=username).first()

        if user and user.check_password(password):
            login_user(user)
            return redirect(url_for("main.dashboard"))

        return "Invalid credentials"

    return render_template_string("""
        <h2>Login</h2>
        <form method="POST">
            Username: <input name="username"><br>
            Password: <input name="password" type="password"><br>
            <button type="submit">Login</button>
        </form>
    """)


@main.route("/dashboard", methods=["GET", "POST"])
@login_required
def dashboard():
    if request.method == "POST":
        exercise = request.form.get("exercise")
        reps = request.form.get("reps")
        weight = request.form.get("weight")

        workout = Workout(
            exercise=exercise,
            reps=int(reps),
            weight=float(weight),
            user_id=current_user.id
        )

        db.session.add(workout)
        db.session.commit()

    workouts = Workout.query.filter_by(user_id=current_user.id).all()

    return render_template_string("""
        <h2>Welcome {{ current_user.username }}</h2>

        <form method="POST">
            Exercise: <input name="exercise"><br>
            Reps: <input name="reps"><br>
            Weight: <input name="weight"><br>
            <button type="submit">Add Workout</button>
        </form>

        <h3>Your Workouts</h3>
        {% for w in workouts %}
            <p>{{ w.exercise }} - {{ w.reps }} reps - {{ w.weight }} kg</p>
        {% endfor %}

        <br>
        <a href="/logout">Logout</a>
    """, workouts=workouts)


@main.route("/logout")
@login_required
def logout():
    logout_user()
    return redirect(url_for("main.home"))