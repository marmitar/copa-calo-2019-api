from flask import jsonify
from werkzeug.exceptions import HTTPException


def typename(obj) -> str:
    """Get the name of the object's type"""
    return type(obj).__name__


class JSONException(HTTPException):
    """
    Base exception for the application.
    Makes a JSON response instead of a HTML one.
    """
    code: int = None
    description: str = None

    def __init__(self, http_exception: HTTPException=None, *, description=None):
        if http_exception:
            self.kind = typename(http_exception)
            self.code = http_exception.code
            self.description = http_exception.description

        else:
            self.kind = typename(self)
            if code:
                self.code = code
            if description:
                self.description=description

        HTTPException.__init__(self)

    def to_dict(self):
        d = {'kind': self.kind}
        if self.code:
            d['code'] = self.code
        if self.description:
            d['description'] = self.description

        return d

    def to_json(self):
        return jsonify(error=self.to_dict())

    def __str__(self):
        if self.description:
            s = f'{self.kind}: {self.description}'
        else:
            s = self.kind

        return s

    def get_response(self, _=None):
        response = self.to_json()
        if self.code:
            response.status_code = self.code
        return response


class InternalServerError(JSONException):
    """Base exception for any non-HTTP exceptions."""
    code = 500
    description = "The server encountered an internal error and was unable to complete your request."

    def __init__(self, error=None):
        description = str(error) if error else None
        JSONException.__init__(self, description=description)
