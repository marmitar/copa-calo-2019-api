from flask_jwt_extended import JWTManager


class JWT(JWTManager):
    def __init__(self):
        JWTManager.__init__(self)
