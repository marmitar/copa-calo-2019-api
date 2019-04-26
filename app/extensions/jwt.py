from flask_jwt_extended import JWTManager

from werkzeug.exceptions import Unauthorized
from app.exceptions import JSONException


class JWT(JWTManager):
    def __init__(self):
        super().__init__()
        self.unauthorized_loader(JWT.unauthorized)

    @staticmethod
    def unauthorized(description):
        return JSONException(Unauthorized(description))
