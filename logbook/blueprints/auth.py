from flask import Blueprint, render_template, redirect, url_for, request, flash, session, g
from logbook.database import db, User
from logbook.forms import LoginForm, RegistrationForm
from werkzeug.security import generate_password_hash, check_password_hash
import functools



bp = Blueprint("auth", __name__)

@bp.route("/login", methods=["POST","GET"])
def login():
    form = LoginForm()

    if form.validate_on_submit():
        user = db.session.execute(db.select(User).filter_by(username=form.username.data)).scalar_one_or_none()
        session.clear()
        session["user_id"] = user.id
        flash("Login Successful!")
        return redirect(url_for("index"))

    return render_template("auth/login.html", form=form)
        

@bp.route("/register", methods=["POST","GET"])
def register():
    form = RegistrationForm()

    if form.validate_on_submit():
        username = request.form.get("username")
        password = request.form.get("password")

        user = User(username=username, password=generate_password_hash(password))
        db.session.add(user)
        db.session.commit()

        flash("New User Registered!")
        return redirect(url_for("auth.login"))

    return render_template("auth/register.html", form=form)


@bp.route("/logout")
def logout():
    session.clear()
    return redirect(url_for("auth.login"))


@bp.before_app_request
def get_user():
    user_id = session.get("user_id")
    g.user = db.session.execute(db.select(User).filter_by(id=user_id)).scalar_one_or_none()


def login_required(view):
    @functools.wraps(view)
    def wrapped_view(**kwargs):
        if g.user is None:
            return redirect(url_for('auth.login'))

        return view(**kwargs)

    return wrapped_view

