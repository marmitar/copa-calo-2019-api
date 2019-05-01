from app.database import SurrogatePK, Model, Column, db, relationship
from app.database.fields import Enum, DateTime, Boolean

from app import tracks
from app.tracks import TrackType, Sex


class Track(Model, SurrogatePK):
    __tablename__ = 'tracks'

    track_type = Column(Enum(TrackType), nullable=False)
    sex = Column(Enum(Sex), nullable=False)

    registrations = relationship('Registration')

    __table_args__ = (db.UniqueConstraint('track_type', 'sex'),)

    # noqa: E303
    def __init__(self, track_type, sex):
        Model.__init__(self, track_type=track_type, sex=sex)
        SurrogatePK.__init__(self)

        self.save()

    @property
    def athletes(self):
        return list(map(lambda r: r.athlete, self.registrations))

    @property
    def name(self):
        return str(self.track_type.value)

    def __repr__(self):
        return f'<Track {self.name}[{self.sex}]>'
