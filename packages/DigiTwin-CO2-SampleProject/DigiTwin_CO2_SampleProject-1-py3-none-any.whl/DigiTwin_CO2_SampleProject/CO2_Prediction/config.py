import datetime
from .sensor import Base
from sqlalchemy.orm import sessionmaker


class Config(object):

    def __init__(self, *args, **kwargs):

        self._engine = None
        self.Base = Base
        self.session = None
        self.time = datetime.datetime.now()

    @property
    def engine(self):
        return self._engine

    @engine.setter
    def engine(self, value):
        self._engine = value
        if self._engine is not None:
            Base.metadata.create_all(self._engine)
            self.session = sessionmaker(bind=self._engine)


db_config = Config()
