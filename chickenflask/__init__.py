"""Initialize Flask app."""
from flask import Flask
from flask_login import LoginManager
from flask_sqlalchemy import SQLAlchemy
from flaskext.markdown import Markdown
from flask_assets import Environment
from config import IS_PRODUCTION

# from ddtrace import patch_all
# https://hackersandslackers.com/flask-application-factory/
# https://hackersandslackers.com/flask-blueprints/

db = SQLAlchemy()
login_manager = LoginManager()
assets_env = Environment()


def init_app():
    """Create Flask application."""
    app = Flask(__name__, instance_relative_config=False)
    config = 'config.ProdConfig' if IS_PRODUCTION else 'config.DevConfig'
    app.config.from_object(config)
    db.init_app(app)
    login_manager.init_app(app)
    assets_env.init_app(app)
    Markdown(app, extensions=['fenced_code'])


    with app.app_context():
        # Import parts of our application
        from .home import routes as home_routes
        from .home import auth as auth_routes
        from .notes import routes as notes_routes

        from .assets import compile_static_assets

        app.register_blueprint(home_routes.home_bp)
        app.register_blueprint(auth_routes.auth_bp, url_prefix='/auth')
        app.register_blueprint(notes_routes.notes_bp, url_prefix='/notes')

        db.create_all()

        compile_static_assets(assets_env)

        return app

