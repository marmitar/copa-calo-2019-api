from dataclasses import dataclass
# from app.database.models import Registration


@dataclass
class Track:
    name: str

    def __repr__(self):
        return self.name

    @property
    def event(self):
        pass

    @property
    def registrations(self):
        pass

    @property
    def athletes(self):
        pass
