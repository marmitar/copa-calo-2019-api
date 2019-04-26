from flask import Flask

from app.commands.urls import urls
from app.commands.lint import lint


def register_commands(app: Flask):
    app.cli.add_command(urls)
    app.cli.add_command(lint)
