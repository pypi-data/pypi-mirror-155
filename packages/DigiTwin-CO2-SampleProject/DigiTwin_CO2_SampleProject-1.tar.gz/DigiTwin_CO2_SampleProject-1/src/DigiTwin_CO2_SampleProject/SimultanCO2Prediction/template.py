import os
from PySimultan import Template, yaml

try:
    import importlib.resources as pkg_resources
except ImportError:
    # Try backported to PY<37 importlib_resources.
    import importlib_resources as pkg_resources


from . import resources


with pkg_resources.path(resources, 'co2_prediction_template.yml') as r_path:
    template_filename = str(r_path)


def create_template():

    database_connection_template = Template(template_name='DatabaseConnection',
                                            template_id='1',
                                            content=['database_name',
                                                     'dialect',
                                                     'driver',
                                                     'host',
                                                     'password',
                                                     'port',
                                                     'user'],
                                            inherits_from='Database',
                                            types={'database_name': 'str',
                                                   'dialect': 'str',
                                                   'driver': 'str',
                                                   'host': 'str',
                                                   'password': 'str',
                                                   'port': 'int',
                                                   'user': 'str'}
                                            )

    window_template = Template(template_name='Window',
                               template_id='2',
                               content=['c_ref',
                                        'gap_width',
                                        'gap_sensor_definition'],
                               inherits_from='SimultanWindow',
                               types={'c_ref': 'float',
                                      'gap_width': 'float'},
                               slots={'gap_sensor_definition': 'Element 3'}
                               )

    zone_template = Template(template_name='Zone',
                             template_id='3',
                             content=['outside_air_temperature_sensor_definition',
                                      'c_outside_sensor_definition',
                                      'room_air_temperature_sensor_definition',
                                      'occupants_sensor_definition',
                                      'c_inside_sensor_definition',
                                      'co2_emission_per_person'],
                             inherits_from='SimultanZone',
                             types={'c_ref': 'float',
                                    'max_gap_width': 'float',
                                    'co2_emission_per_person': 'float'},
                             slots={'outside_air_temperature_sensor_definition': 'Element 4',
                                    'c_outside_sensor_definition': 'Element 3',
                                    'occupants_sensor_definition': 'Element 2',
                                    'c_inside_sensor_definition': 'Element 1',
                                    'room_air_temperature_sensor_definition': 'Element 0'
                                    }
                             )

    sensor_definition_template = Template(template_name='Sensor',
                                          template_id='4',
                                          content=['db_id',
                                                   'measured_parameter',
                                                   'query',
                                                   'refresh_interval',
                                                   'database'],
                                          types={'id': 'float',
                                                 'measured_parameter': 'str',
                                                 'query': 'str',
                                                 'refresh_interval': 'float'},
                                          slots={'database': 'Element 0'}
                                          )

    co2_prediction_definition_template = Template(template_name='CO2_Prediction_Definition',
                                                  template_id='5',
                                                  inherits_from='SimultanPredictionDefinition',
                                                  content=['zones',
                                                           'prediction_interval',
                                                           'prediction_timesteps'],
                                                  types={'prediction_interval': 'float',
                                                         'prediction_timesteps': 'float'},
                                                  slots={'zones': 'Liste 0'}
                                                  )

    if not os.path.isfile(template_filename):
        open(template_filename, 'a').close()
    with open(template_filename,
              mode='w',
              encoding="utf-8") as f_obj:
        yaml.dump([database_connection_template, window_template, zone_template, sensor_definition_template, co2_prediction_definition_template], f_obj)
