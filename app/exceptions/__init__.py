from flask import Flask, jsonify
from werkzeug.exceptions import HTTPException, default_exceptions

from app.exceptions.json_exception import JSONException
from app.exceptions.internal_error import InternalServerError


def register_errorhandlers(app: Flask):
    for code in default_exceptions.keys():
        app.register_error_handler(code, adapt_exception)


def adapt_exception(error):
    if isinstance(error, JSONException):
        return error

    elif isinstance(error, HTTPException):
        return JSONException.from_exception(error)

    return InternalServerError(error)
