from app.exceptions import JSONException


class MissingArguments(JSONException):
    code = 400
    description = 'Request missing arguments'

    def __init__(self, *args):
        super().__init__(missing=list(args))
