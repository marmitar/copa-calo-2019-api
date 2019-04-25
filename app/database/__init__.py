from app.extensions import db
from sqlalchemy.orm import relationship


Model = db.Model
Column = db.Column


class SurrogatePK:
    """Adds a surrogate integer 'primary key' column named ``id``"""
    __table_args__ = {'extend_existing': True}

    id = Column(db.Integer, primary_key=True, index=True)

    @classmethod
    def get_by_id(cls, record_id):
       return cls.query.get(int(record_id))
