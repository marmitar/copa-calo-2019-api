from flask import Flask


def create_app(config_object={}):
    """Application factory"""
    app = Flask(__name__.split('.')[0])
    app.url_map.strict_slashes = False
    app.config.from_object(config_object)

    register_extensions(app)
    register_blueprints(app)
    register_errorhandlers(app)
    register_shellcontext(app)
    register_commands(app)
    return app


def register_extensions(app: Flask):
    pass


def register_blueprints(app: Flask):
    pass


def register_errorhandlers(app: Flask):
    pass


def register_shellcontext(app: Flask):
    context = {}

    app.shell_context_processor(lambda: context)


def register_commands(app: Flask):
    pass
