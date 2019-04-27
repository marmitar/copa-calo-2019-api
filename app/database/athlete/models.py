from enum import Enum, auto, unique

from app.database import SurrogatePK, Model, Column, reference_col, db
from app.database.fields import String, Boolean
from app.database.models import College
from app.exceptions import protect_params


@unique
class Sex(Enum):
    fem = auto()
    masc = auto()


class Athlete(Model, SurrogatePK):
    __tablename__ = 'athletes'

    name = Column(String(64), unique=True, nullable=False)
    rg = Column(String(16), unique=True, nullable=False)
    sex = Column(db.Enum(Sex), nullable=False)
    extra = Column(Boolean, nullable=False)

    college_id = reference_col(College)

    # noqa: E303
    def __init__(self, name, rg, sex, extra, college):
        Model.__init__(self, name=name, rg=rg, sex=sex, extra=extra, college=college)
        SurrogatePK.__init__(self)

        self.save()

    @property
    def college(self) -> College:
        return College.get_by_id(self.college_id)

    @college.setter
    def college(self, user_college: College):
        self.college_id = user_college.id

    @property
    def college_initials(self):
        return self.college.initials

    def update(self, **kwargs):
        kwargs = {key: val for key, val in kwargs.items() if val is not None}
        super().update(**kwargs)

    def __repr__(self):
        return f'<Athlete {self.name}>'
