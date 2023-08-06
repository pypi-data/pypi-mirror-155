from sqlalchemy import create_engine, engine
from sqlalchemy.orm import sessionmaker
from .sensor import Base


class Database(object):

    def __init__(self, *args, **kwargs):
        """

        see: https://docs.sqlalchemy.org/en/14/core/engines.html

        :param args:
        :param kwargs:
        @keyword DatabaseName: Name of the Database; if using sqlite this is the full filename
        @keyword Dialect: Database dialect;
        Valid dialects are for Example: 'sqlite', 'postgres', 'mysql', 'oracle', 'mssql'
        @keyword Driver: Database driver; postgresql: 'psycopg2', 'pg8000'; mysql: 'mysqldb', 'pymysql'
        """
        self.database_name = kwargs.get('database_name')
        ''':type: str'''

        self.dialect = kwargs.get('dialect')
        ''':type: str'''

        self.driver = kwargs.get('driver')
        ''':type: str'''

        self.host = kwargs.get('host')
        ''':type: str'''

        self.password = kwargs.get('password', None)
        ''':type: str'''

        self.port = kwargs.get('port', None)
        ''':type: int'''

        self.user = kwargs.get('user', None)
        ''':type: str'''

        self._engine = None
        self._url = None
        self.sessionmaker = None
        self.session_scope = None
        self._session = None

        self.echo = kwargs.get('echo', False)

    @property
    def engine(self):
        if self._engine is None:
            self.connect()
        return self._engine

    @engine.setter
    def engine(self, value):
        self._engine = value
        if engine is not None:
            Base.metadata.create_all(self._engine)
            self.sessionmaker = sessionmaker(bind=self._engine)
            self.session = self.sessionmaker()

    @property
    def session(self):
        if self.engine is None:
            raise Exception(f'Unable to connect {self}')
        return self._session

    @session.setter
    def session(self, value):
        self._session = value

    @property
    def url(self):
        if self._url is None:
            self._url = self.make_url()
        return self._url

    @url.setter
    def url(self, value):
        self._url = value

    def make_url(self):

        if self.driver is not None:
            drivername = self.dialect + self.driver
        else:
            drivername = self.dialect

        if not self.user:
            user = None
        else:
            user = self.user

        if not self.password:
            password = None
        else:
            password = self.password

        if not self.host:
            host = None
        else:
            host = self.host

        if not self.port:
            port = None
        else:
            port = self.port

        if not self.database_name:
            database_name = None
        else:
            database_name = self.database_name

        return engine.URL(drivername=drivername,
                          username=user,
                          password=password,
                          host=host,
                          port=port,
                          database=database_name)

    def connect(self):
        self.engine = create_engine(self.url, pool_pre_ping=True, echo=self.echo)

    def query_all(self, cls):
        return self.session.query(cls).all()

    def get_session(self):
        return self.session_scope

    def add(self, obj):
        self.session.add(obj)
        self.session.commit()
