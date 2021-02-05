"""Initialize Flask app."""
from flask import Flask
from flask_login import LoginManager
from flask_sqlalchemy import SQLAlchemy
from flaskext.markdown import Markdown

# from ddtrace import patch_all
# https://hackersandslackers.com/flask-application-factory/
# https://hackersandslackers.com/flask-blueprints/

db = SQLAlchemy()
login_manager = LoginManager()


def init_app():
    """Create Flask application."""
    app = Flask(__name__, instance_relative_config=False)
    app.config.from_object("config.DevConfig")

    db.init_app(app)
    login_manager.init_app(app)
    Markdown(app, extensions=['fenced_code'])

    # assets = Environment()
    # assets.init_app(app)

    with app.app_context():
        # Import parts of our application
        from .home import routes as home_routes
        from .home import auth as auth_routes

        #from .assets import compile_static_assets

        # Register Blueprints
        app.register_blueprint(home_routes.home_bp)
        app.register_blueprint(auth_routes.auth_bp)

        db.create_all()

        # Compile static assets
        #compile_static_assets(assets)

        return app

