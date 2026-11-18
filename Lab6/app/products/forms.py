from flask_wtf import FlaskForm
from flask_wtf.file import FileField, FileAllowed
from wtforms import (
    StringField,
    TextAreaField,
    DecimalField,
    SelectField,
    IntegerField,
    SubmitField,
)
from wtforms.validators import DataRequired, Length, NumberRange

PRODUCT_CATEGORIES = [
    ("Electronics", "Electronics"),
    ("Computers", "Computers"),
    ("Smartphones", "Smartphones"),
    ("Accessories", "Accessories"),
    ("Other", "Other"),
]


class ProductForm(FlaskForm):
    name = StringField(
        "Назва товару",
        validators=[
            DataRequired(message="Введіть назву товару."),
            Length(min=3, message="Назва товару повинна містити мінімум 3 символи."),
        ],
    )
    content = TextAreaField(
        "Опис товару",
        validators=[DataRequired(message="Введіть опис товару.")],
        render_kw={"rows": 5, "cols": 40},
    )
    price = DecimalField(
        "Ціна ($)",
        places=2,
        validators=[
            DataRequired(message="Введіть ціну товару."),
            NumberRange(min=0.01, message="Ціна повинна бути додатною."),
        ],
    )
    category = SelectField(
        "Категорія",
        choices=PRODUCT_CATEGORIES,
        validators=[DataRequired(message="Оберіть категорію товару.")],
    )
    quantity = IntegerField(
        "Кількість одиниць",
        default=0,
        validators=[
            NumberRange(min=0, message="Кількість не може бути від'ємною."),
        ],
    )
    image = FileField(
        "Зображення товару (PNG, JPG, JPEG)",
        validators=[
            FileAllowed(["png", "jpg", "jpeg"], "Дозволені лише формати PNG, JPG та JPEG!")
        ],
    )
    submit = SubmitField("Зберегти товар")
