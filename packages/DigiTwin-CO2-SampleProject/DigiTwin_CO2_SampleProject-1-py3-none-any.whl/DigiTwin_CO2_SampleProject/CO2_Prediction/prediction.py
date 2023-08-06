from datetime import datetime, timedelta
import numpy as np
import matplotlib as mpl
import matplotlib.dates as mdates
import matplotlib.pyplot as plt

mpl.use('TkAgg')


def init_plot(zones):

    fig, axs = plt.subplots(zones.__len__(), 1,
                            constrained_layout=True,
                            sharex=True,
                            figsize=(15, 10))

    if not isinstance(axs, list):
        axs = [axs]

    plots = [None] * zones.__len__()
    # plt.rcParams['axes.titlepad'] = -14  # pad is in points...

    for i, zone in enumerate(zones):
        axs[i].set_title(zone.name,  loc='left', fontsize=7)
        axs[i].set_ylabel('CO2-Concentration in ppm', fontsize=7)
        axs[i].grid(True)
        axs[i].xaxis.set_major_formatter(mdates.DateFormatter('%H:%M:%S'))
        plots[i] = axs[i].plot_date([], [], 'r-')[0]
        for label in axs[i].get_xticklabels(which='major'):
            label.set(rotation=30, horizontalalignment='right')

    return fig, axs, plots


class PredictionDefinition(object):

    def __init__(self, *args, **kwargs):

        self.zones = kwargs.get('zones', [])
        self.prediction_interval = kwargs.get('prediction_interval', 30)
        self.prediction_timesteps = kwargs.get('prediction_interval', np.array([30, 60, 120, 300, 600, 1800]))

    def run_predictions(self):

        fig, axs, plots = init_plot(self.zones)

        while True:

            for i, zone in enumerate(self.zones):
                now = datetime.now()
                pred_times = [now + timedelta(seconds=x) for x in self.prediction_timesteps.values.flatten()]
                values = zone.calculate_co2_concentration(self.prediction_timesteps.values.flatten()).tolist()
                axs[i].plot_date(pred_times, values, 'k--', linewidth=0.1, zorder=0)
                axs[i].relim()
                axs[i].autoscale_view()


                zone_co2_data = plots[i].get_data()
                plots[i].set_data(np.append(zone_co2_data[0], now).tolist(), np.append(zone_co2_data[1], float(zone.c_inside)).tolist())

            fig.canvas.draw()
            fig.canvas.flush_events()
            plt.pause(1)
