from app.database import SurrogatePK, Model, Column, db, relationship, reference_col
from app.database.fields import DateTime, Boolean, String, Enum

from app.database.models import Track
from app.exceptions import InvalidParameter

from app.tracks import Status


class Event(Model, SurrogatePK):
    __tablename__ = 'events'

    track_id = reference_col(Track, index=True)
    name = Column(String(60), nullable=False, index=True)

    status = Column(Enum(Status), nullable=False, default=Status.not_started)
    time = Column(DateTime, nullable=False)

    last_ev_id = reference_col('Event', nullable=True, unique=True)
    next_ev_id = reference_col('Event', nullable=True, unique=True)

    __table_args__ = (db.UniqueConstraint('track_id', 'name'),)

    # noqa: E303
    def __init__(self, track, name, time, status=None):
        if not status:
            status = Status.not_started
        Model.__init__(self, track=track, name=name, time=time, status=status)
        SurrogatePK.__init__(self)

        self.save()

    @property
    def track(self):
        return Track.get_by_id(self.track_id)

    @track.setter
    def track(self, track):
        self.track_id = track.id

    @property
    def last_ev(self):
        return Track.get_by_id(self.last_ev_id)

    @last_ev.setter
    def last_ev(self, last):
        if (last.time >= self.time):
            raise InvalidParameter('evento anterior')
        self.last_ev_id = last.id

        if (last.next_ev_id != self.id):
            last.next_ev = self

    @property
    def last_ev_name(self):
        if self.last_ev:
            return self.last_ev.name

    @property
    def next_ev(self):
        return Track.get_by_id(self.next_ev_id)

    @next_ev.setter
    def next_ev(self, next_):
        self.next_ev_id = next_.id

        if (next_.next_ev_id != self.id):
            next_.next_ev = self

    @property
    def track_type(self):
        return self.track.track_type

    def __repr__(self):
        return f'<Event {self.name} of {self.track_type}>'
