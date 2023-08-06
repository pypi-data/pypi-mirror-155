import datetime
from typing import Union
from sqlalchemy.orm import declarative_base, reconstructor
from sqlalchemy.orm import relationship
from sqlalchemy.orm.session import Session
from sqlalchemy import Column, Integer, Float, TIMESTAMP, String, ForeignKey
from .logger import logger


Base = declarative_base()


class Measurement(Base):

    __tablename__ = 'measurements'

    date = Column(TIMESTAMP, nullable=False, default=datetime.datetime.now)
    id = Column(Integer, primary_key=True, autoincrement=True)
    value = Column(Float)

    sensor_id = Column(Integer, ForeignKey('sensors.id'))
    sensor = relationship("Sensor", back_populates="measurements")


class Sensor(Base):

    __tablename__ = 'sensors'

    id = Column(Integer, primary_key=True)
    name = Column(String)
    measured_parameter = Column(String)
    measurements = relationship("Measurement", back_populates="sensor")
    refresh_interval = Column(Float)

    def __init__(self, *args, **kwargs):
        """

        :param args:
        :param kwargs:
        @keyword ID: Sensor ID
        :type ID: int
        @keyword MeasuredParameter: Name of the measured parameter; Example: 'Room Temperature'
        :type MeasuredParameter: str
        @keyword Query: Query which returns all measurements; Example: 'SELECT * FROM Measures WHERE sensor_id = 1'
        :type Query: str
        @keyword Database: Database with the measurements table
        :type Database: CO2_Prediction.Database
        @keyword refresh_interval: values are automatically updated if time since last update exceeds refresh_interval; in microseconds
        :type float
        @keyword do_refresh: if True values are automatically updated
        """

        self.id = kwargs.get('id')
        ''':type: int'''

        self.name = kwargs.get('name')
        ''':type: Name'''

        self.measured_parameter = kwargs.get('measured_parameter')
        ''':type: str'''

        self.query = kwargs.get('query')
        ''':type: str'''

        self.refresh_interval = kwargs.get('refresh_interval', 10)
        ''':type: float'''

        self.last_refresh = datetime.datetime.now()

        self._latest_measurement = None
        self._latest_measurement_value = None
        self.last_latest_measurement_refresh = datetime.datetime.now()
        self.last_latest_measurement_value_refresh = datetime.datetime.now()

        self.do_refresh = True

    @reconstructor
    def init_on_load(self):
        self.last_refresh = datetime.datetime.now()
        self._latest_measurement = None
        self._latest_measurement_value = None
        self.last_latest_measurement_refresh = datetime.datetime.now()
        self.last_latest_measurement_value_refresh = datetime.datetime.now()
        self.do_refresh = True

    @property
    def latest_measurement(self):
        dt = (datetime.datetime.now() - self.last_latest_measurement_refresh).microseconds * 1000
        logger.debug(f'{self.name}: time since latest measurement update: {dt} s')

        if (dt > self.refresh_interval) or (self._latest_measurement is None):
            logger.info(f'{self.name}: latest measurement expired. Updating latest measurement...')
            self.last_latest_measurement_refresh = datetime.datetime.now()
            session = Session.object_session(self)
            self._latest_measurement = session.query(Measurement).filter(Measurement.sensor_id == self.id).order_by(Measurement.id.desc()).first()
        return self._latest_measurement

    @property
    def latest_measurement_value(self):
        dt = (datetime.datetime.now() - self.last_latest_measurement_value_refresh).microseconds
        logger.debug(f'{self.name}: time since latest measurement value update: {dt} s')
        if (dt > self.refresh_interval) or (self._latest_measurement_value is None):
            logger.info(f'{self.name}: latest measurement value expired. Updating latest measurement value...')
            self.last_latest_measurement_value_refresh = datetime.datetime.now()
            session = Session.object_session(self)
            value = session.query(Measurement.value).filter(Measurement.sensor_id == self.id).order_by(
                Measurement.id.desc()).first()
            if value is not None:
                self._latest_measurement_value = value[0]
            else:
                self._latest_measurement_value = None

        return self._latest_measurement_value

    @property
    def num_measurements(self):
        return self.measurements.__len__()

    def _get_created_by(self):
        return datetime.datetime.now()

    def create_measurement(self, value: Union[int, float]):

        session = Session.object_session(self)

        measurement = Measurement(sensor=self, value=value)
        session.add(measurement)
        session.commit()

        return measurement

    def __getattribute__(self, item):
        # if item == 'refresh_interval':
        #     object.__getattribute__(self, item)
        # else:
        #     if self.refresh_interval is None:
        #         return object.__getattribute__(self, item)

        if (item == 'measurements') and (self.do_refresh):
            if hasattr(self, 'last_refresh'):
                if (datetime.datetime.now() - self.last_refresh).microseconds > self.refresh_interval:
                    logger.info(f'{self.name}: measurements expired. Updating measurements...')
                    session = Session.object_session(self)
                    session.refresh(self)
        return object.__getattribute__(self, item)


# @event.listens_for(Sensor, 'load')
# def receive_load(target, context):
#     target.last_refresh = datetime.datetime.now()
#     target.last_latest_measurement_refresh = target.last_refresh
