from app.database import SurrogatePK, Model, Column, db, reference_col, relationship
from app.database.fields import Enum, DateTime, Boolean, Integer, Text

from app import tracks
from app.database.models import Event, Athlete
from app.exceptions.models import InvalidResource


class Result(Model, SurrogatePK):
    __tablename__ = 'results'

    event_id = reference_col(Event, index=True)
    athlete_id = reference_col(Athlete, index=True)

    value = Column(Integer, nullable=True)
    removed = Column(Boolean, nullable=False, default=False)
    reason = Column(Text, nullable=True)

    results = relationship('Result')

    __table_args__ = (db.UniqueConstraint('event_id', 'athlete_id'),)

    # noqa: E303
    def __init__(self, event, athlete, value=None, removed=None, reason=None):
        if not removed:
            removed = False
        else:
            value = None

        if event.track not in athlete.tracks:
            raise InvalidResource('atleta não está inscrito nesta prova')

        Model.__init__(self, event=event, athlete=athlete, value=value, remove=removed, reason=reason)
        SurrogatePK.__init__(self)

        self.save()

    @property
    def event(self):
        return Event.get_by_id(self.event_id)

    @event.setter
    def event(self, other):
        self.event_id = other.id

    @property
    def athlete(self):
        return Athlete.get_by_id(self.athlete_id)

    @athlete.setter
    def athlete(self, other):
        self.athlete_id = other.id

    @property
    def track(self):
        return self.event.track

    def __repr__(self):
        return f'<Result {self.athlete.name} on {self.event.track_type}>'
