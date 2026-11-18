from datetime import datetime
import os
import uuid
from flask import (
    current_app,
    render_template,
    request,
    redirect,
    url_for,
    flash,
    abort,
)
from tinydb import TinyDB, Query
from werkzeug.utils import secure_filename
from . import products_bp
from .forms import ProductForm

INITIAL_PRODUCTS = [
    {
        "id": 1,
        "name": "Laptop",
        "price": 1200.00,
        "category": "Computers",
        "quantity": 5,
        "image": "",
        "created_at": "2026-10-15 12:00:00",
        "content": "Потужний ноутбук з процесором Intel Core i7, 16 ГБ оперативної пам’яті та SSD на 512 ГБ.",
    },
    {
        "id": 2,
        "name": "Phone",
        "price": 800.00,
        "category": "Smartphones",
        "quantity": 12,
        "image": "",
        "created_at": "2026-10-15 12:05:00",
        "content": "Смартфон із 6.5-дюймовим OLED-дисплеєм, подвійною камерою та акумулятором на 5000 мА·год.",
    },
    {
        "id": 3,
        "name": "PC",
        "price": 1800.00,
        "category": "Computers",
        "quantity": 3,
        "image": "",
        "created_at": "2026-10-15 12:10:00",
        "content": "Настільний комп’ютер для ігор або роботи з графікою: RTX 4070, 32 ГБ RAM, 1 ТБ SSD.",
    },
]


def get_products_table():
    db_path = current_app.config.get("PRODUCTS_DB_PATH", "data/products.json")
    os.makedirs(os.path.dirname(db_path), exist_ok=True)
    db = TinyDB(db_path, ensure_ascii=False, indent=4)
    table = db.table("products")
    if len(table) == 0 and not current_app.config.get("SKIP_SEED_PRODUCTS", False):
        table.insert_multiple(INITIAL_PRODUCTS)
    return db, table


def _save_uploaded_image(file_storage) -> str:
    if not file_storage or not getattr(file_storage, "filename", ""):
        return ""
    filename = secure_filename(file_storage.filename)
    _, ext = os.path.splitext(filename)
    unique_name = f"{uuid.uuid4().hex}{ext.lower()}"
    upload_dir = os.path.join(products_bp.root_path, "static", "uploads")
    os.makedirs(upload_dir, exist_ok=True)
    file_storage.save(os.path.join(upload_dir, unique_name))
    return f"uploads/{unique_name}"


@products_bp.route("/product", methods=["GET"])
@products_bp.route("/products/", methods=["GET"])
@products_bp.route("/products", methods=["GET"])
def product_list():
    db, table = get_products_table()
    products = table.all()
    db.close()
    return render_template("products/products.html", products=products)


@products_bp.route("/product/add", methods=["GET", "POST"])
def product_add():
    form = ProductForm()
    if form.validate_on_submit():
        db, table = get_products_table()
        all_items = table.all()
        next_id = max((item.get("id", 0) for item in all_items), default=0) + 1
        image_path = _save_uploaded_image(form.image.data)

        new_product = {
            "id": next_id,
            "name": form.name.data.strip(),
            "content": form.content.data.strip(),
            "price": round(float(form.price.data), 2),
            "category": form.category.data,
            "quantity": int(form.quantity.data),
            "image": image_path,
            "created_at": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
        }
        table.insert(new_product)
        db.close()
        flash(f"Товар '{new_product['name']}' успішно додано!", "success")
        return redirect(url_for("products.product_list"))
    elif request.method == "POST":
        flash("Перевірте правильність заповнення форми товару.", "danger")

    return render_template("products/product_form.html", form=form, title="Додати товар", is_edit=False)


@products_bp.route("/product/<int:id>", methods=["GET"])
@products_bp.route("/products/<int:id>", methods=["GET"])
def product_detail(id):
    db, table = get_products_table()
    ProductQuery = Query()
    product = table.get(ProductQuery.id == id)
    db.close()
    if product is None:
        abort(404)
    return render_template("products/detail_product.html", product=product)


@products_bp.route("/product/<int:id>/edit", methods=["GET", "POST"])
def product_edit(id):
    db, table = get_products_table()
    ProductQuery = Query()
    product = table.get(ProductQuery.id == id)
    if product is None:
        db.close()
        abort(404)

    form = ProductForm()
    if request.method == "GET":
        form.name.data = product["name"]
        form.content.data = product["content"]
        form.price.data = product["price"]
        form.category.data = product["category"]
        form.quantity.data = product["quantity"]
    elif form.validate_on_submit():
        new_image = _save_uploaded_image(form.image.data)
        updated_fields = {
            "name": form.name.data.strip(),
            "content": form.content.data.strip(),
            "price": round(float(form.price.data), 2),
            "category": form.category.data,
            "quantity": int(form.quantity.data),
            "image": new_image if new_image else product.get("image", ""),
        }
        table.update(updated_fields, ProductQuery.id == id)
        db.close()
        flash(f"Товар '{updated_fields['name']}' успішно оновлено!", "success")
        return redirect(url_for("products.product_detail", id=id))
    else:
        flash("Перевірте правильність заповнення форми редагування.", "danger")

    db.close()
    return render_template(
        "products/product_form.html",
        form=form,
        product=product,
        title="Редагувати товар",
        is_edit=True,
    )


@products_bp.route("/product/<int:id>/delete", methods=["POST"])
def product_delete(id):
    db, table = get_products_table()
    ProductQuery = Query()
    product = table.get(ProductQuery.id == id)
    if product is None:
        db.close()
        abort(404)

    table.remove(ProductQuery.id == id)
    db.close()
    flash(f"Товар '{product['name']}' успішно видалено!", "info")
    return redirect(url_for("products.product_list"))
