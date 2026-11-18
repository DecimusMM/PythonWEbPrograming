from flask import (
    request,
    render_template,
    redirect,
    url_for,
    session,
    flash,
    make_response,
)
from . import users_bp

USERS = {
    "user1": "password123",
    "admin": "admin123",
    "maksym": "pass123",
}


@users_bp.route("/hi/<string:name>")  # /users/hi/ivan?age=45
def greetings(name):
    name = name.upper()
    age = request.args.get("age", None, int)
    return render_template("users/hi.html", name=name, age=age)


@users_bp.route("/admin")
def admin():
    to_url = url_for("users.greetings", name="administrator", age=45, _external=True)
    return redirect(to_url)


@users_bp.route("/login", methods=["GET", "POST"])
def login():
    if request.method == "POST":
        username = request.form.get("username", "").strip()
        password = request.form.get("password", "")
        if username in USERS and USERS[username] == password:
            session["username"] = username
            flash(f"Ласкаво просимо, {username}! Ви успішно увійшли.", "success")
            return redirect(url_for("users.profile"))
        else:
            flash("Wrong data! Try again!", "danger")
            return redirect(url_for("users.login"))
    return render_template("users/login.html")


@users_bp.route("/logout", methods=["GET", "POST"])
def logout():
    session.pop("username", None)
    flash("Ви успішно вийшли з системи.", "info")
    return redirect(url_for("users.login"))


@users_bp.route("/profile", methods=["GET", "POST"])
def profile():
    if "username" not in session:
        flash("Доступ заборонено! Будь ласка, увійдіть у систему.", "danger")
        return redirect(url_for("users.login"))

    if request.method == "POST":
        action = request.form.get("action")
        resp = make_response(redirect(url_for("users.profile")))

        if action == "add_cookie":
            key = request.form.get("cookie_key", "").strip()
            value = request.form.get("cookie_value", "").strip()
            max_age_raw = request.form.get("cookie_max_age", "").strip()
            if key:
                max_age = int(max_age_raw) if max_age_raw.isdigit() else None
                resp.set_cookie(key, value, max_age=max_age)
                flash(f"Кукі '{key}' успішно додано!", "success")
            else:
                flash("Ключ кукі не може бути порожнім.", "warning")
            return resp

        elif action == "delete_cookie":
            key = request.form.get("delete_key", "").strip()
            if key and key in request.cookies:
                resp.delete_cookie(key)
                flash(f"Кукі '{key}' успішно видалено!", "success")
            else:
                flash(f"Кукі з ключем '{key}' не знайдено.", "warning")
            return resp

        elif action == "delete_all_cookies":
            deleted_count = 0
            for key in request.cookies:
                if key != "session":
                    resp.delete_cookie(key)
                    deleted_count += 1
            flash(f"Усі кукі користувача ({deleted_count}) успішно видалено!", "info")
            return resp

    theme = request.cookies.get("theme", session.get("theme", "light"))
    return render_template(
        "users/profile.html",
        username=session["username"],
        cookies=request.cookies,
        theme=theme,
    )


@users_bp.route("/theme/<string:theme>", methods=["GET", "POST"])
def set_theme(theme):
    if "username" not in session:
        flash("Доступ заборонено! Будь ласка, увійдіть у систему.", "danger")
        return redirect(url_for("users.login"))

    if theme not in ("light", "dark"):
        theme = "light"

    session["theme"] = theme
    resp = make_response(redirect(url_for("users.profile")))
    resp.set_cookie("theme", theme, max_age=30 * 24 * 3600)
    flash(f"Кольорову схему змінено на '{theme}'.", "info")
    return resp
