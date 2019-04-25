from flask_jwt_extended import JWTManager


class JWT(JWTManager):
    def __init__(self):
        super().__init__()
