import enum
from app.database import SurrogatePK, Model, Column, reference_col, db
from app.database.fields import String, Binary, Enum
from app.extensions import bcrypt
from app.database.college import College

from app.exceptions.models import InvalidPassword


@enum.unique
class Permision(enum.Enum):
    admin = enum.auto()
    dm = enum.auto()
    arbiter = enum.auto()


class User(Model, SurrogatePK):
    __tablename__ = 'users'

    username = Column(String(32), unique=True, nullable=False, index=True)
    password_hash = Column(Binary(60), unique=True, nullable=False)

    college_id = reference_col(College, nullable=True)
    permission = Column(Enum(Permision), nullable=False, default=Permision.dm)

    token: str = None

    # noqa: E303
    def __init__(self, username, password, permission, college=None):
        Model.__init__(self, username=username, password=password, permission=permission, college=college)
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

    def is_admin(self):
        return self.permission == Permision.admin

    def is_dm(self):
        return self.permission == Permision.dm

    def is_arbiter(self):
        return self.permission == Permision.arbiter

    @property
    def college(self) -> College:
        if self.college_id:
            return College.get_by_id(self.college_id)

    @college.setter
    def college(self, user_college: College):
        if user_college:
            self.college_id = user_college.id

    @property
    def college_initials(self):
        if self.college_id:
            return self.college.initials

    def __repr__(self):
        return f'<User {self.username}>'
