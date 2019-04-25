from flask import Flask

from app.config import ProdConfig
from app.extensions import register_extensions
from app.exceptions import register_errorhandlers
from app.extensions.shell import register_shellcontext


def create_app(config=ProdConfig):
    """Application factory"""
    app = Flask(app_name())
    app.config.from_object(config)

    register_extensions(app)
    register_blueprints(app)
    register_errorhandlers(app)
    register_shellcontext(app)
    register_commands(app)
    return app


def app_name():
    import_name = __name__
    import_path = import_name.split('.')
    import_root = import_path[0]
    return import_root



def register_blueprints(app: Flask):
    pass


def register_commands(app: Flask):
    pass
