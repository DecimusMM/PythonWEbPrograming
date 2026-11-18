from flask import request, render_template, flash, redirect, url_for
from . import app


@app.route('/')
def main():
    return render_template("index.html")


@app.route('/homepage')
def home():
    """View for the Home page of your website."""
    agent = request.user_agent
    return render_template("homepage.html", agent=agent)


@app.route('/resume')
def resume():
    return render_template("resume.html", title="Резюме")


@app.route('/contacts', methods=['GET', 'POST'])
def contacts():
    if request.method == 'POST':
        flash("Дякуємо! Повідомлення прийнято (демо-режим).", "success")
        return redirect(url_for("contacts"))
    return render_template("contacts.html", title="Контакти")
