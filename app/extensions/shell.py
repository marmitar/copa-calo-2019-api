from flask import Flask

from app.extensions import db, jwt, bcrypt, cache, cors
from app.database import models


def register_shellcontext(app: Flask):
    shell_context = {
        'db': db,
        'jwt': jwt,
        'bcrypt': bcrypt,
        'cache': cache,
        'cors': cors,
        'app': app,

        'User': models.User,
        'Permission': models.Permision,
        'College': models.College,
        'Athlete': models.Athlete,
        'Track': models.Track,
        'Registration': models.Registration
    }

    app.shell_context_processor(lambda: shell_context)
