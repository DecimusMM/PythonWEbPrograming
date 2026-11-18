import os
from flask import Flask, render_template
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from sqlalchemy.orm import DeclarativeBase
from dotenv import load_dotenv
from .config import config

load_dotenv()


class Base(DeclarativeBase):
    pass


db = SQLAlchemy(model_class=Base)
migrate = Migrate()


def create_app(config_name: str | None = None) -> Flask:
    if config_name is None:
        config_name = os.environ.get("FLASK_ENV", "default")

    app = Flask(__name__)
    cfg_class = config.get(config_name, config["default"])
    app.config.from_object(cfg_class)

    db.init_app(app)
    migrate.init_app(app, db)

    from .views import register_main_routes
    register_main_routes(app)

    from .users import users_bp
    from .products import products_bp
    from .posts import post_bp

    app.register_blueprint(users_bp)
    app.register_blueprint(products_bp)
    app.register_blueprint(post_bp, url_prefix="/post")

    @app.errorhandler(404)
    def not_found(e):
        return render_template("404.html"), 404

    return app
