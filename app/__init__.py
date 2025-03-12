from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from app.config import Config

db = SQLAlchemy()
migrate = Migrate()

def create_app():
    app = Flask(__name__)
    app.config.from_object(Config)

    db.init_app(app)
    migrate.init_app(app, db)

    # Import models to ensure they are recognized by Alembic
    from app.models import UsersData  # ✅ Ensure this line is present!

    # Import and register routes
    from app.routes import register_routes
    register_routes(app)

    return app
