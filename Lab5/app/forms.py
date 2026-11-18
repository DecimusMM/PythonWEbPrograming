from flask_wtf import FlaskForm
from wtforms import StringField, SelectField, TextAreaField, SubmitField
from wtforms.validators import DataRequired, Length, Email, Regexp

SUBJECT_CHOICES = [
    ("general", "Загальне питання"),
    ("cooperation", "Співпраця"),
    ("support", "Технічна підтримка"),
    ("feedback", "Відгук"),
]


class ContactForm(FlaskForm):
    name = StringField(
        "Name",
        validators=[
            DataRequired(message="Ім'я є обов'язковим полем."),
            Length(min=4, max=10, message="Довжина імені має бути від 4 до 10 символів."),
        ],
    )
    email = StringField(
        "Email",
        validators=[
            DataRequired(message="Email є обов'язковим полем."),
            Email(message="Введіть коректну адресу електронної пошти."),
        ],
    )
    phone = StringField(
        "Phone",
        validators=[
            DataRequired(message="Телефон є обов'язковим полем."),
            Regexp(
                r"^\+380\d{9}$",
                message="Телефон має бути у форматі +380XXXXXXXXX (9 цифр після +380).",
            ),
        ],
    )
    subject = SelectField(
        "Subject",
        choices=SUBJECT_CHOICES,
        validators=[DataRequired(message="Оберіть тему повідомлення.")],
    )
    message = TextAreaField(
        "Message",
        validators=[
            DataRequired(message="Повідомлення є обов'язковим полем."),
            Length(max=500, message="Повідомлення не може перевищувати 500 символів."),
        ],
        render_kw={"rows": 5},
    )
    submit = SubmitField("Send Message")
