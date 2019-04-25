import datetime as dt

from app.database import db, SurrogatePK, Model, Column
from app.extensions import bcrypt

from app.database.user.exceptions import InvalidPassword


class User(Model, SurrogatePK):
    __tablename__ = 'users'

    username = Column(db.String(32), unique=True, nullable=False)
    email = Column(db.String(100), unique=True, nullable=False, index=True)
    password_hash = Column(db.Binary(128), unique=True, nullable=False)

    criado_em = Column(db.DateTime, nullable=False, default=dt.datetime.utcnow)
    atualizado_em = Column(db.DateTime, nullable=False, default=dt.datetime.utcnow, onupdate=dt.datetime.utcnow)

    token: str = ''


    def __init__(self, username, email, password):
        Model.__init__(self, username=username, email=email, password=password)

    @property
    def password(self):
        raise AttributeError('cannot access password directly')

    @password.setter
    def password(self, new_password: str):
        hashed = bcrypt.generate_password_hash(new_password)
        self.password_hash = hashed

    def valid_password(self, password) -> bool:
        return bcrypt.check_password_hash(self.password_hash, password)

    def update(self, old_password, **kwargs):
        if not self.valid_password(old_password):
            raise InvalidPassword

        Model.update(self, **kwargs)

    def delete(self, password):
        if not self.valid_password(password):
            raise InvalidPassword

        Model.delete(self)

    def __repr__(self):
        return f'<User {self.username}>'
