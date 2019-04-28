from app.database import SurrogatePK, Model, Column, reference_col, db
from app.database.fields import Enum
from app.exceptions import protect_params, InvalidParameter

from app.database.models import Athlete, Track


class Registration(Model, SurrogatePK):
    __tablename__ = 'registrations'

    athlete_id = reference_col(Athlete, index=True)
    track_id = reference_col(Track, index=True)

    __table_args__ = (db.UniqueConstraint('athlete_id', 'track_id'),)

    # noqa: E303
    def __init__(self, athlete, track):
        if track.sex != athlete.sex:
            raise InvalidParameter('sex')

        Model.__init__(self, athlete=athlete, track=track)
        SurrogatePK.__init__(self)

        self.save()

    @property
    def athlete(self) -> Athlete:
        return Athlete.get_by_id(self.athlete_id)

    @athlete.setter
    def athlete(self, new_athl):
        self.athlete_id = new_athl.id

    @property
    def athlete_rg(self, name):
        return self.athlete.rg

    @property
    def track(self) -> Track:
        return Track.get_by_id(self.track_id)

    @track.setter
    def track(self, new_track):
        self.track_id = new_track.id

    def __repr__(self):
        return f'<Registration of {self.athlete.name} on {self.track}>'
