from app.exceptions import JSONException


class InternalServerError(JSONException):
    code = 500
    description = "The server encountered an internal error and was unable to complete your request."

    def __init__(self, error=None):
        description = None
        if error:
            description = str(error)

        JSONException.__init__(self, description=description)
