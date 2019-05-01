from app.database import SurrogatePK, Model, Column, reference_col, relationship, db
from app.database.fields import String, Boolean, Enum
from app.database.models import College
from app.exceptions import protect_params
from app.tracks import Sex


class Athlete(Model, SurrogatePK):
    __tablename__ = 'athletes'

    name = Column(String(64), nullable=False)
    rg = Column(String(20), nullable=False, index=True)
    rg_orgao = Column(String(10), nullable=False)
    sex = Column(Enum(Sex), nullable=False)

    college_id = reference_col(College)

    registrations = relationship('Registration')
    results = relationship('Result')

    __table_args__ = (db.UniqueConstraint('rg', 'rg_orgao'),)

    # noqa: E303
    def __init__(self, name, rg, rg_orgao, sex, college):
        Model.__init__(self, name=name, rg=rg, rg_orgao=rg_orgao, sex=sex, college=college)
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

    @property
    def tracks(self):
        return list(map(lambda r: r.track, self.registrations))

    def update(self, **kwargs):
        kwargs = {key: val for key, val in kwargs.items() if val is not None}
        super().update(**kwargs)

    def __repr__(self):
        return f'<Athlete {self.name}>'
