from app.database import SurrogatePK, Model, Column, reference_col
from app.database.fields import String, Binary
from app.extensions import bcrypt
from app.database.college import College

from app.exceptions.users import InvalidPassword


class User(Model, SurrogatePK):
    __tablename__ = 'users'

    username = Column(String(32), unique=True, nullable=False, index=True)
    password_hash = Column(Binary(60), unique=True, nullable=False)

    college_id = reference_col(College, nullable=False)

    access_token: str = None
    refresh_token: str = None

    # noqa: E303
    def __init__(self, username, password, college):
        Model.__init__(self, username=username, password=password, college=college)
        SurrogatePK.__init__(self)

        self.save()

    @property
    def password(self):
        raise AttributeError('cannot access password directly')

    @password.setter
    def password(self, new_password: str):
        hashed = bcrypt.generate_password_hash(new_password)
        self.password_hash = hashed

    def valid_password(self, password) -> bool:
        return bcrypt.check_password_hash(self.password_hash, password)

    @property
    def college(self):
        return College.get_by_id(self.college_id)

    @college.setter
    def college(self, user_college: College):
        self.college_id = user_college.id

    @property
    def college_initials(self):
        return self.college.initials

    def update(self, old_password, new_password):
        if not self.valid_password(old_password):
            raise InvalidPassword

        self.password = new_password

    def delete(self, password):
        if not self.valid_password(password):
            raise InvalidPassword

        super().delete()

    def __repr__(self):
        return f'<User {self.username}>'
