from app.database.schema import Schema, fields, validate, EnumField, pre_dump

from app.tracks import TrackType


class RegistrationSchema(Schema):

    athleteName = fields.String(
        attribute  = 'athlete_name',
        allow_none = False,
        load_only  = True
    )

    athleteRg = fields.String(
        attribute  = 'athlete_rg',
        allow_none = False,
        load_only  = True
    )

    track = EnumField(
        TrackType,
        allow_none = False,
        load_only  = True
    )

    trackName = fields.String(
        attribute  = 'track_name',
        allow_none = False,
        dump_only  = True,
    )

    extra = fields.Boolean(
        allow_none = True
    )

    bestMark = fields.Float(
        attribute  = 'best_mark',
        allow_none = True
    )

    athlete = fields.Nested(
        'AthleteSchema',
        exclude = ('tracks',),
        allow_none = False,
        dump_only = True
    )

    @pre_dump
    def get_track_type(self, reg):
        class Result:
            def __init__(self, registration):
                self.regist = registration

            def __getattr__(self, key):
                if key != 'track':
                    return getattr(self.regist, key)
                return self.regist.track.track_type

        return Result(reg)
