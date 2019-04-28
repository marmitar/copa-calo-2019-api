from flask import Flask

from app.extensions import db, jwt, bcrypt, cache, cors
from app.database import models


shell_context = {
    'db': db,
    'jwt': jwt,
    'bcrypt': bcrypt,
    'cache': cache,
    'cors': cors,

    'User': models.User,
    'College': models.College,
    'Athlete': models.Athlete
}


def register_shellcontext(app: Flask):
    app.shell_context_processor(lambda: shell_context)
