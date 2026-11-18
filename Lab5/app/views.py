import logging
import os
from flask import request, render_template, flash, redirect, url_for
from . import app
from .forms import ContactForm


def _log_contact_submission(form: ContactForm) -> None:
    log_path = app.config.get("CONTACTS_LOG_PATH", "logs/contacts.log")
    os.makedirs(os.path.dirname(log_path), exist_ok=True)
    logger = logging.getLogger("contact_logger")
    logger.setLevel(logging.INFO)
    if not any(isinstance(h, logging.FileHandler) and h.baseFilename == os.path.abspath(log_path) for h in logger.handlers):
        handler = logging.FileHandler(log_path, encoding="utf-8")
        formatter = logging.Formatter("%(asctime)s | %(levelname)s | %(message)s")
        handler.setFormatter(formatter)
        logger.addHandler(handler)
    logger.info(
        "Name=%s | Email=%s | Phone=%s | Subject=%s | Message=%s",
        form.name.data,
        form.email.data,
        form.phone.data,
        form.subject.data,
        form.message.data,
    )


@app.route("/")
def main():
    return render_template("index.html")


@app.route("/homepage")
def home():
    """View for the Home page of your website."""
    agent = request.user_agent
    return render_template("homepage.html", agent=agent)


@app.route("/resume")
def resume():
    return render_template("resume.html", title="Резюме")


@app.route("/contact", methods=["GET", "POST"])
@app.route("/contacts", methods=["GET", "POST"])
def contact():
    form = ContactForm()
    if form.validate_on_submit():
        _log_contact_submission(form)
        flash(
            f"Дякуємо, {form.name.data}! Ваше повідомлення успішно відправлено та записано в лог.",
            "success",
        )
        return redirect(url_for("contact"))
    elif request.method == "POST":
        flash("Помилка валідації форми! Перевірте введені дані.", "danger")
    return render_template("contacts.html", title="Контакти", form=form)
