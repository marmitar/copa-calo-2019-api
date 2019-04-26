from flask_jwt_extended import JWTManager


class JWT(JWTManager):
    def __init__(self):
        super().__init__()

    def set_identity(self, cls, *, id_attr, id_loader):
        get_id_by_user = lambda user: getattr(user, id_attr)
        get_user_by_id = lambda id: getattr(cls, id_loader)(id)

        self.user_identity_loader(get_id_by_user)
        self.user_loader_callback_loader(get_user_by_id)
