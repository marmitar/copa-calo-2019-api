from flask import jsonify
from werkzeug.exceptions import HTTPException


def typename(obj):
    return type(obj).__name__


class JSONException(HTTPException):
    code: int = None
    description: str = None

    def __init__(self, code=None, description=None):
        self.kind = typename(self)

        if code:
            self.code = code
        if description:
            self.description = description

        HTTPException.__init__(self, description=description)

    @staticmethod
    def from_exception(exception):
        new = JSONException(exception.code, exception.description)
        new.kind = typename(exception)
        return new

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


