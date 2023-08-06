import sys
import numpy as np
import matplotlib as mpl
import matplotlib.dates as mdates
import matplotlib.pyplot as plt
import datetime
import argparse
from ..main import load_project
from ..SimultanCO2Prediction.simultan_adaptions import get_sensor
from .utils import sinus_value_fcn, static_value_fcn, random_range_value_fcn, sinus_int_value_fcn

mpl.use('TkAgg')


def init_plot(sensors):

    fig, axs = plt.subplots(sensors.__len__(), 1,
                            constrained_layout=True,
                            sharex=True,
                            figsize=(15, 10))

    # plt.rcParams['axes.titlepad'] = -14  # pad is in points...

    plots = [None] * sensors.__len__()
    value_lists = [([datetime.datetime.now()], [0])] * sensors.__len__()

    for i, sensor in enumerate(sensors):
        sensor.do_refresh = False
        axs[i].set_title(sensor.name,  loc='left', fontsize=12)
        axs[i].set_ylabel(sensor.measured_parameter, fontsize=10)
        axs[i].grid(True)
        axs[i].xaxis.set_major_formatter(mdates.DateFormatter('%H:%M:%S'))
        plots[i] = axs[i].plot_date([], [], '-')[0]
        for label in axs[i].get_xticklabels(which='major'):
            label.set(rotation=30, horizontalalignment='right')

    return fig, axs, plots, value_lists


def fake_measurement_data(project_file=None):
    parser = argparse.ArgumentParser(prog='fake_measurement_data',
                                     description='Programm which creates fake measurement data for sensors in a SIMULTAN project')
    parser.add_argument('-project', nargs='?', help='Absolute project path')
    args = parser.parse_args()

    if project_file is None:
        project_file = args.project

    template_parser, data_model = load_project(project_file=project_file)

    typed_data = data_model.get_typed_data(template_parser=template_parser, create_all=True)

    sensor_definitions = template_parser.template_classes['Sensor'].cls_instances

    sensors = [get_sensor(x) for x in sensor_definitions]

    sensor_value_generators = {'default': random_range_value_fcn(0, 1),
                               0: sinus_value_fcn(amp=5, freq=1/60),
                               1: static_value_fcn(5),
                               2: random_range_value_fcn(0, 10),
                               'Gap Width': sinus_value_fcn(shift=0.5, amp=0.5, freq=1 / 300),
                               'Room CO2 Concentration': sinus_value_fcn(shift=1000, amp=50, freq=1/(15*60)),
                               'Outside Air Temperature': sinus_value_fcn(shift=0, amp=10, freq=1/(60*60)),
                               'Occupants': sinus_int_value_fcn(shift=5, amp=5, freq=1/(10*60)),
                               'Room Air Temperature': sinus_value_fcn(shift=20, amp=2, freq=1/(15*60)),
                               'Outside CO2 Concentration': sinus_value_fcn(shift=460, amp=50, freq=1/(30*60))}

    # initialize plot
    fig, axs, plots, value_lists = init_plot(sensors)

    ii = 0

    while True:
        ii += 1
        val_str = f'Created Measurement {ii}:  '

        for i, sensor in enumerate(sensors):

            now = datetime.datetime.now()

            if sensor.measurements:
                t_0 = sensor.measurements[0].date
            else:
                t_0 = datetime.datetime.now()
            dt = datetime.datetime.now() - t_0

            if sensor.measured_parameter in sensor_value_generators.keys():
                val = sensor_value_generators[sensor.measured_parameter](time=dt.seconds)
            else:
                val = sensor_value_generators['default'](time=dt.seconds)
            measurement = sensor.create_measurement(val)

            data = plots[i].get_data()
            plots[i].set_data(np.append(data[0], now).tolist(), np.append(data[1], float(val)).tolist())
            val_str += f'{measurement.value}  |  '
            axs[i].relim()
            axs[i].autoscale_view()

        fig.canvas.draw()
        fig.canvas.flush_events()
        plt.pause(5)

    sys.exit()
