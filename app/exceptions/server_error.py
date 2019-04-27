from app.exceptions import JSONException


class InternalServerError(JSONException):
    """Base exception for any non-HTTP exceptions."""
    code = 500
    description = "The server encountered an internal error and was unable to complete your request."

    def __init__(self, error=None):
        kwargs = {}
        if error:
            kwargs['internalError'] = str(error)
        super().__init__(**kwargs)


class ForbiddenAccess(JSONException):
    code = 403
    description = "You can't do that"
