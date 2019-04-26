from flask_sqlalchemy import SQLAlchemy, Model


class Database(SQLAlchemy):
    def __init__(self):

        class CRUDModel(Model):
            def __init__(_self, *args, **kwargs):
                super().__init__(*args, **kwargs)

            @classmethod
            def create(cls, **kwargs):
                instance = cls(**kwargs)
                instance.save()
                return instance

            def update(_self, commit=True, **kwargs):
                for attr, value in kwargs.items():
                    setattr(_self, attr, value)
                if commit:
                    _self.save()

            def save(_self, commit=True):
                self.session.add(_self)
                if commit:
                    self.session.commit()

            def delete(_self, commit=True):
                self.session.delete(_self)
                if commit:
                    self.session.commit()

        super().__init__(model_class=CRUDModel)
