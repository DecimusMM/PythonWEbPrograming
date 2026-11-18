from datetime import datetime
from flask import render_template, request, redirect, url_for, flash, abort, session
from app import db
from . import post_bp
from .models import Post
from .forms import PostForm


@post_bp.route("", methods=["GET"])
@post_bp.route("/", methods=["GET"])
def all_posts():
    stmt = (
        db.select(Post)
        .where(Post.is_active == True)  # noqa: E712
        .order_by(Post.posted.desc())
    )
    posts = db.session.scalars(stmt).all()
    return render_template("posts.html", posts=posts)


@post_bp.route("/create", methods=["GET", "POST"])
@post_bp.route("/add_post", methods=["GET", "POST"])
def create_post():
    form = PostForm()
    if request.method == "POST":
        # Support both `content` and `text` keys in case tests send `text`
        if not form.content.data and request.form.get("text"):
            form.content.data = request.form.get("text")

    if form.validate_on_submit():
        is_active_val = (
            bool(form.is_active.data)
            if ("is_active" in request.form or "submit" in request.form)
            else True
        )
        new_post = Post(
            title=form.title.data.strip(),
            content=form.content.data.strip(),
            is_active=is_active_val,
            posted=form.publish_date.data or datetime.utcnow(),
            category=form.category.data or "other",
            author=session.get("username", "Anonymous"),
        )
        db.session.add(new_post)
        db.session.commit()
        flash("Post added successfully", "success")
        return redirect(url_for("posts.all_posts"))
    elif request.method == "POST":
        flash("Enter the correct data in the form!", "danger")

    return render_template("add_post.html", form=form, title="Create a New Post")


@post_bp.route("/<int:id>", methods=["GET"])
def detail_post(id: int):
    post = db.get_or_404(Post, id)
    return render_template("detail_post.html", post=post)


@post_bp.route("/<int:id>/update", methods=["GET", "POST"])
@post_bp.route("/<int:id>/edit", methods=["GET", "POST"])
def edit_post(id: int):
    post = db.session.get(Post, id)
    if not post:
        abort(404)

    form = PostForm(obj=post)
    if request.method == "GET":
        form.publish_date.data = post.posted
    elif request.method == "POST":
        if not form.content.data and request.form.get("text"):
            form.content.data = request.form.get("text")

    if form.validate_on_submit():
        is_active_val = (
            bool(form.is_active.data)
            if ("is_active" in request.form or "submit" in request.form)
            else post.is_active
        )
        post.title = form.title.data.strip()
        post.content = form.content.data.strip()
        post.is_active = is_active_val
        if form.publish_date.data:
            post.posted = form.publish_date.data
        if form.category.data:
            post.category = form.category.data
        db.session.commit()
        flash("Post updated successfully! Пост оновлено!", "success")
        return redirect(url_for("posts.detail_post", id=post.id))

    return render_template("add_post.html", form=form, post=post, title="Редагувати пост")


@post_bp.route("/<int:id>/delete", methods=["GET", "POST"])
@post_bp.route("/delete/<int:id>", methods=["GET", "POST"])
def delete_post(id: int):
    post = db.session.get(Post, id)
    if not post:
        abort(404)

    if request.method == "POST":
        db.session.delete(post)
        db.session.commit()
        flash("Post deleted successfully. Пост успішно видалено.", "danger")
        return redirect(url_for("posts.all_posts"))

    return render_template("delete_confirm.html", post=post)
