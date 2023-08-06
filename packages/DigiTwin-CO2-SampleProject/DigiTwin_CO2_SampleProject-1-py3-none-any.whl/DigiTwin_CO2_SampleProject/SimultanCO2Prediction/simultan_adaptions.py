import numpy as np

from ..CO2_Prediction.database import Database
from ..CO2_Prediction.window import Window
from ..CO2_Prediction.zone import Zone
from ..CO2_Prediction.sensor import Sensor
from ..CO2_Prediction.prediction import PredictionDefinition

from PySimultan.default_types import BuildInFace, BuildInVolume


class SimultanDatabase(Database):

    def __init__(self, *args, **kwargs):

        self._engine = None
        self._url = None
        self.sessionmaker = None
        self.session_scope = None
        self._session = None

        self.echo = kwargs.get('echo', False)

        self._sensors = None

    @property
    def sensors(self):
        if self._sensors is None:
            self._sensors = self.query_all(Sensor)
        return self._sensors


class SimultanWindow(Window, BuildInFace):

    def __init__(self, *args, **kwargs):
        BuildInFace.__init__(self, *args, **kwargs)

        self._gap_sensor = None

    @property
    def b(self):
        # get the lower points. Assumption: window is rectangular
        points = self.geo_instances[0].points
        idx = np.argpartition(points[:, 2], 2)
        return np.linalg.norm(points[idx[1], :] - points[idx[0], :])

    @property
    def h(self):
        points = self.geo_instances[0].points
        return np.linalg.norm(points[np.argmax(points[:, 2]), :] - points[np.argmin(points[:, 2]), :])

    @property
    def gap_sensor(self):
        if self._gap_sensor is None:
            sensor = get_sensor(self.gap_sensor_definition)
            self._gap_sensor = sensor
        return self._gap_sensor


class SimultanZone(Zone):

    def __init__(self, *args, **kwargs):

        self._outside_air_temperature_sensor = None
        self._room_air_temperature_sensor = None
        self._c_outside_sensor = None
        self._c_inside_sensor = None
        self._occupants_sensor = None

    @property
    def v_a(self):
        zone_geo_object = next((x for x in self.contained_components if isinstance(x, BuildInVolume)), None)
        return zone_geo_object.v_a

    @property
    def windows(self):

        zone_geo_object = next((x for x in self.contained_components if isinstance(x, BuildInVolume)), None)

        windows = []
        for face in zone_geo_object.geo_faces:
            for component in face.components:
                if isinstance(component, SimultanWindow):
                    windows.append(component)

        return windows

    @property
    def outside_air_temperature_sensor(self):
        if self._outside_air_temperature_sensor is None:
            sensor = get_sensor(self.outside_air_temperature_sensor_definition)
            self._outside_air_temperature_sensor = sensor
        return self._outside_air_temperature_sensor

    @property
    def c_outside_sensor(self):
        if self._c_outside_sensor is None:
            sensor = get_sensor(self.c_outside_sensor_definition)
            self._c_outside_sensor = sensor
        return self._c_outside_sensor

    @property
    def occupants_sensor(self):
        if self._occupants_sensor is None:
            sensor = get_sensor(self.occupants_sensor_definition)
            self._occupants_sensor = sensor
        return self._occupants_sensor

    @property
    def c_inside_sensor(self):
        if self._c_inside_sensor is None:
            sensor = get_sensor(self.c_inside_sensor_definition)
            self._c_inside_sensor = sensor
        return self._c_inside_sensor

    @property
    def room_air_temperature_sensor(self):
        if self._room_air_temperature_sensor is None:

            sensor = get_sensor(self.room_air_temperature_sensor_definition)
            self._room_air_temperature_sensor = sensor

        return self._room_air_temperature_sensor


class SimultanPredictionDefinition(PredictionDefinition):

    def __init__(self, *args, **kwargs):
        pass


def get_sensor(sensor_definition):
    database = sensor_definition.database
    sensor_id = int(sensor_definition.db_id)

    sensors = database.query_all(Sensor)
    sensor = next((x for x in sensors if x.id == sensor_id), None)

    if sensor is None:
        init_dict = {'id': sensor_definition.db_id,
                     'name': sensor_definition.name,
                     'measured_parameter': sensor_definition.measured_parameter,
                     'query': sensor_definition.query,
                     'refresh_interval': sensor_definition.refresh_interval}

        sensor = Sensor(**init_dict)
        database.add(sensor)

    return sensor
