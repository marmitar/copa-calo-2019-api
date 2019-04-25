"""Create an application instance."""

from flask import helpers

from app import create_app
from app.config import DevConfig, ProdConfig


if helpers.get_env().startswith('dev'):
    app = create_app(config=DevConfig)

elif helpers.get_env().startswith('prod'):
    app = create_app(config=ProdConfig)
