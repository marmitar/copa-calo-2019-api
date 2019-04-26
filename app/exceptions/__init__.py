from flask import Flask, jsonify
from werkzeug.exceptions import HTTPException, default_exceptions

from app.exceptions.json_exception import JSONException
from app.exceptions.server_error import InternalServerError
from app.exceptions.missing_args import MissingArguments

from app.exceptions.require_args import require_args


def register_errorhandlers(app: Flask):
    for code in default_exceptions.keys():
        app.register_error_handler(code, adapt_exception)


def adapt_exception(error):
    if isinstance(error, JSONException):
        return error

    elif isinstance(error, HTTPException):
        return JSONException(error)

    return InternalServerError(error)
