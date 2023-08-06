import numpy as np

from PySimultan.data_model import *
from PySimultan.template_tools import TemplateParser

from .SimultanCO2Prediction import SimultanDatabase, SimultanWindow, SimultanZone, SimultanPredictionDefinition
from .SimultanCO2Prediction import resources

import argparse

try:
    import importlib.resources as pkg_resources
except ImportError:
    # Try backported to PY<37 importlib_resources.
    import importlib_resources as pkg_resources


def load_project(project_file: str = None):
    """
    Load a simultan Project
    :param project_file: absolute path of the project
    :return: template_parser, data_model
    """
    with pkg_resources.path(resources, 'co2_prediction_template.yml') as r_path:
        template_file = str(r_path)

    template_parser = TemplateParser(template_filepath=template_file)
    template_parser.bases['Database'] = SimultanDatabase
    template_parser.bases['SimultanWindow'] = SimultanWindow
    template_parser.bases['SimultanZone'] = SimultanZone
    template_parser.bases['SimultanPredictionDefinition'] = SimultanPredictionDefinition

    template_parser.create_template_classes()
    data_model = DataModel(project_path=project_file)
    # typed_data = data_model.get_typed_data(template_parser=template_parser)

    return template_parser, data_model


def run_predictions(project_file: str = None):

    parser = argparse.ArgumentParser(prog='run_calc_co2_predictions',
                                     description='Program which calculates simple CO2 predictions for zones'
                                                 'using live measurements in a SIMULTAN project')
    parser.add_argument('-project', nargs='?', help='Absolute project path')
    args = parser.parse_args()

    if project_file is None:
        project_file = args.project

    template_parser, data_model = load_project(project_file=project_file)
    typed_data = data_model.get_typed_data(template_parser=template_parser, create_all=True)

    prediction_definition = template_parser.template_classes['CO2_Prediction_Definition'].cls_instances[0]
    prediction_definition.run_predictions()

    print('done')
