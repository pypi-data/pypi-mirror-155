from typing import Union
import numpy as np


class Window(object):

    def __init__(self, *args, **kwargs):
        """

        :param args:
        :param kwargs:
        """
        self.name = kwargs.get('name', 'unnamed window')
        self.b = kwargs.get('b')    # window width in m
        self.h = kwargs.get('h')  # window height in m

        self.c_ref = kwargs.get('c_ref')  # Exchange coefficient in [m^0.5 / h * K^0.5]; see ÖNORM 8110-3

        self.gap_width = kwargs.get('max_gap_width')
        self.gap_sensor = kwargs.get('gap_sensor')  # Exchange coefficient in [m^0.5 / h * K^0.5]; see ÖNORM 8110-3

    @property
    def total_gap_width(self):
        return self.gap_sensor.latest_measurement_value * self.gap_width

    def calc_a_eff(self) -> float:
        """
        Calculate Effective ventilation opening in m²; see ÖNORM 8110-3
        :return: Effective ventilation opening in m²
        """
        return self.total_gap_width * (self.b + self.h)

    def calc_volume_flow_rate(self,
                              t_out: Union[int, float],
                              t_in: Union[int, float]) -> float:
        """
        Calculate the air volume flow rate over a window according to ÖNORM 8110-3
        :param t_out: Outside temperature in °C
        :param t_in: Inside temperature in °C
        :return: volume_flow_rate over the window in m³/s
        """
        a_eff = self.calc_a_eff()
        return 0.7 * self.c_ref * a_eff * np.sqrt(self.h) * np.sqrt(np.abs(t_in - t_out)) / 3600

    def __repr__(self):
        return "{}({!r})".format(self.__class__.__name__, self.name)
