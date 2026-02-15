from flask import Blueprint, render_template, redirect, url_for, request, flash
from flask_login import login_user, logout_user, login_required, current_user
from app.models import User, Workout, db
from werkzeug.security import generate_password_hash, check_password_hash

main = Blueprint("main", __name__)

@main.route("/")
def home():
    return redirect(url_for("main.login"))

# ---------------- REGISTER ----------------
@main.route("/register", methods=["GET", "POST"])
def register():
    if request.method == "POST":
        username = request.form.get("username")
        password = request.form.get("password")

        if not username or not password:
            flash("All fields are required")
            return redirect(url_for("main.register"))

        existing_user = User.query.filter_by(username=username).first()
        if existing_user:
            flash("Username already exists")
            return redirect(url_for("main.register"))

        hashed_password = generate_password_hash(password)
        new_user = User(username=username, password=hashed_password)
        db.session.add(new_user)
        db.session.commit()

        return redirect(url_for("main.login"))

    return render_template("register.html")


# ---------------- LOGIN ----------------
@main.route("/login", methods=["GET", "POST"])
def login():
    if request.method == "POST":
        username = request.form.get("username")
        password = request.form.get("password")

        if not username or not password:
            flash("All fields required")
            return redirect(url_for("main.login"))

        user = User.query.filter_by(username=username).first()

        if user and check_password_hash(user.password, password):
            login_user(user)
            return redirect(url_for("main.dashboard"))
        else:
            flash("Invalid credentials")
            return redirect(url_for("main.login"))

    return render_template("login.html")


# ---------------- DASHBOARD ----------------
@main.route("/dashboard", methods=["GET", "POST"])
@login_required
def dashboard():

    if request.method == "POST":
        exercise = request.form.get("exercise")
        reps = request.form.get("reps")
        weight = request.form.get("weight")

        if not exercise or not reps or not weight:
            flash("All workout fields required")
            return redirect(url_for("main.dashboard"))

        new_workout = Workout(
            exercise=exercise,
            reps=int(reps),
            weight=float(weight),
            user_id=current_user.id
        )

        db.session.add(new_workout)
        db.session.commit()

        return redirect(url_for("main.dashboard"))

    workouts = Workout.query.filter_by(user_id=current_user.id).all()
    return render_template("dashboard.html", workouts=workouts)


# ---------------- DELETE ----------------
@main.route("/delete/<int:id>")
@login_required
def delete_workout(id):
    workout = Workout.query.get_or_404(id)

    if workout.user_id != current_user.id:
        return redirect(url_for("main.dashboard"))

    db.session.delete(workout)
    db.session.commit()

    return redirect(url_for("main.dashboard"))


# ---------------- LOGOUT ----------------
@main.route("/logout")
@login_required
def logout():
    logout_user()
    return redirect(url_for("main.login"))