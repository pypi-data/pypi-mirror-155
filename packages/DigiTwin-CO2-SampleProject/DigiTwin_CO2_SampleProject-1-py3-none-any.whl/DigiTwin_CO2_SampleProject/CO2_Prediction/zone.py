import numpy as np
import numpy.typing as npt

from .utils import convert_l_h_to_mg_s, convert_ppm_to_mg_m3, convert_mg_m3_to_ppm


class Zone(object):

    def __init__(self, *args, **kwargs):

        self.name = kwargs.get('name', 'unnamed zone')

        self.v_a = kwargs.get('v_a')                    # zone volume in m³
        self.windows = kwargs.get('windows', [])        # List of zone windows
        self.occupants_sensor = kwargs.get('occupants_sensor')        # number of occupants

        self.room_air_temperature_sensor = kwargs.get('room_air_temperature_sensor')           # Room air temperature in °C
        self.outside_air_temperature_sensor = kwargs.get('outside_air_temperature_sensor')    # Outside air temperature in °C

        self.co2_emission_per_person = kwargs.get('co2_emission_per_person', 20.4)  # CO2 emission per Person in l/h

        self.c_inside_sensor = kwargs.get('c_inside_sensor')     # CO2 Concentration inside the room in ppm
        self.c_outside_sensor = kwargs.get('c_outside_sensor')   # CO2 Concentration outside

    @property
    def occupants(self):
        return self.occupants_sensor.latest_measurement_value

    @property
    def room_air_temperature(self):
        return self.room_air_temperature_sensor.latest_measurement_value

    @property
    def outside_air_temperature(self):
        return self.outside_air_temperature_sensor.latest_measurement_value

    @property
    def c_inside(self):
        return self.c_inside_sensor.latest_measurement_value

    @property
    def c_outside(self):
        return self.c_outside_sensor.latest_measurement_value

    def calculate_co2_concentration(self, t: npt.ArrayLike):

        # calculate fresh air volume flow rate:
        v_aul = sum([x.calc_volume_flow_rate(self.outside_air_temperature, self.room_air_temperature) for x in self.windows])

        # calculate CO2 emission in the zone:
        e_co2 = self.occupants * convert_l_h_to_mg_s(self.co2_emission_per_person)

        c_out_mg_m3 = convert_ppm_to_mg_m3(self.c_outside)
        c_in_mg_m3 = convert_ppm_to_mg_m3(self.c_inside)

        c_mg_m3 = (c_out_mg_m3 + (e_co2 / v_aul)) + (c_in_mg_m3 - c_out_mg_m3 - e_co2 / v_aul) * np.exp(-(v_aul/self.v_a) * t)

        return convert_mg_m3_to_ppm(c_mg_m3)
