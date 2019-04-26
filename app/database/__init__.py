from app.extensions import db


Model = db.Model
Column = db.Column

relationship = db.relationship
backref = db.backref


class SurrogatePK:
    """Adds a surrogate integer 'primary key' column named ``id``"""
    __table_args__ = {'extend_existing': True}

    id = Column(db.Integer, primary_key=True, index=True)

    @classmethod
    def get_by_id(cls, id):
        return cls.query.get(int(id))

    @classmethod
    def check_by_key_value(cls, **kwargs):
        return db.session.query(cls.id).filter_by(**kwargs).scalar() is not None
