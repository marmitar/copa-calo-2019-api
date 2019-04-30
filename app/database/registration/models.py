from app.database import SurrogatePK, Model, Column, reference_col, db
from app.database.fields import Enum, Float, Boolean
from app.exceptions import protect_params, InvalidParameter

from app.database.models import Athlete, Track


class Registration(Model, SurrogatePK):
    __tablename__ = 'registrations'

    athlete_id = reference_col(Athlete, index=True)
    track_id = reference_col(Track, index=True)

    extra = Column(Boolean, nullable=False, default=False)
    best_mark = Column(Float(), nullable=True)

    __table_args__ = (db.UniqueConstraint('athlete_id', 'track_id'),)

    # noqa: E303
    def __init__(self, athlete, track, best_mark=None, extra=None):
        if track.sex != athlete.sex:
            raise InvalidParameter('sex')
        if not extra:
            extra = False

        Model.__init__(self, athlete=athlete, track=track, best_mark=best_mark, extra=extra)
        SurrogatePK.__init__(self)

        self.save()

    @property
    def athlete(self) -> Athlete:
        return Athlete.get_by_id(self.athlete_id)

    @athlete.setter
    def athlete(self, new_athl):
        self.athlete_id = new_athl.id

    @property
    def athelte_name(self):
        return self.athlete.name

    @property
    def track(self) -> Track:
        return Track.get_by_id(self.track_id)

    @track.setter
    def track(self, new_track):
        self.track_id = new_track.id

    @property
    def track_name(self):
        return self.track.name

    def __repr__(self):
        return f'<Registration of {self.athlete.name} on {self.track}>'
