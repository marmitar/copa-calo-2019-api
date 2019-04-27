from flask_sqlalchemy import SQLAlchemy, Model


class Database(SQLAlchemy):
    def __init__(self):

        class CRUDModel(Model):
            def __init__(model_self, *args, **kwargs):  # noqa: N805
                super().__init__(*args, **kwargs)

            @classmethod
            def create(cls, **kwargs):
                instance = cls(**kwargs)
                instance.save()
                return instance

            def update(model_self, commit=True, **kwargs):  # noqa: N805
                for attr, value in kwargs.items():
                    setattr(model_self, attr, value)
                if commit:
                    model_self.save()

            def save(model_self, commit=True):  # noqa: N805
                self.session.add(model_self)
                if commit:
                    self.session.commit()

            def delete(model_self, commit=True):  # noqa: N805
                self.session.delete(model_self)
                if commit:
                    self.session.commit()

            @classmethod
            def get(cls, unique=True, **kwargs):
                result = cls.query.filter_by(**kwargs)
                if unique:
                    result = result.first()

                return result

        super().__init__(model_class=CRUDModel)
