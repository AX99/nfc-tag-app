from flask import Flask
from firebase_admin import firestore
from src.firebase_init.firebase_init import initialize_firebase
from src.routes.tag_routes import tag_routes
from src.routes.finder_routes import finder_routes  # Import finder_routes
from src.firebase_manager import FirebaseManager
from src.config import FIREBASE_DB_ID


def create_app(config_object=None):  # Allow for optional config object
    app = Flask(__name__)

    # Load config from object, environment variables, or default values
    if config_object:
        app.config.from_object(config_object)
    app.config.from_envvar("APP_SETTINGS", silent=True)  # Load from environment
    if "FIREBASE_DB_ID" not in app.config:  # Default Value if not set
        app.config["FIREBASE_DB_ID"] = FIREBASE_DB_ID

    db = initialize_firebase(app.config["FIREBASE_DB_ID"])
    app.db = db

    manager = FirebaseManager(db)
    app.manager = manager

    app.register_blueprint(tag_routes, url_prefix="/api")
    app.register_blueprint(finder_routes, url_prefix="/api")

    return app
