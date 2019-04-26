from app.extensions import jwt

from app.database.user import User


jwt.set_identity(User, id_attr='id', id_loader='get_by_id')
