from flask import Flask, render_template, request, flash, redirect, url_for

app = Flask(__name__)
app.secret_key = "dev-secret-key"  # для flash-повідомлень (навчальний проєкт)


@app.route("/")
@app.route("/resume")
def resume():
    return render_template("resume.html", title="Резюме")


@app.route("/contacts", methods=["GET", "POST"])
def contacts():
    if request.method == "POST":
        # Форма-заглушка: реальна відправка не виконується
        flash("Дякуємо! Повідомлення прийнято (демо-режим, без реальної відправки).", "success")
        return redirect(url_for("contacts"))
    return render_template("contacts.html", title="Контакти")


if __name__ == "__main__":
    app.run(debug=True)
