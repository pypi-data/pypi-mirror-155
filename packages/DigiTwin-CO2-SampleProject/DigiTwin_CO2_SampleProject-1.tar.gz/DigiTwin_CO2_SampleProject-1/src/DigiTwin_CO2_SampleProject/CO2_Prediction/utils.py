from typing import Union


def convert_l_h_to_mg_s(value: Union[int, float]) -> Union[int, float]:
    """
    Convert CO2 emission from l/h in mg/s
    :param value: CO2 emission in l/h
    """

    return value * 1963 / 3600


def convert_ppm_to_mg_m3(c_ppm,
                         mol_mass: Union[int, float] = None,
                         mol_vol: Union[int, float] = None):
    """
    converts concentration in ppm to concentration in mg/m³
    :param c_ppm:       concentration in ppm (parts per million)
    :param mol_mass:    molar mass of the component; default is 44.01 g/mol for CO2
    :param mol_vol:     molar volume of the component; default is 24.471 L/mol for CO2
    :return c_mg_m3:    concentration in mg/m³
    """

    # molar volume of 24,471 if None is given
    if mol_vol is None:
        mol_vol = 24.471

    # Molar mass of CO2 if None is given
    if mol_mass is None:
        mol_mass = 44.01

    c_mg_m3 = c_ppm * mol_mass / mol_vol

    return c_mg_m3


def convert_mg_m3_to_ppm(c_mg_m3: Union[int, float],
                         mol_mass: Union[int, float] = None,
                         mol_vol: Union[int, float] = None) -> Union[int, float]:
    """
    converts concentration in ppm to concentration in mg/m³
    :param c_mg_m3:     concentration in mg/m³
    :param mol_mass:    molar mass of the component; default is 44.01 g/mol for CO2
    :param mol_vol:     molar volume of the component; default is 24.471 L/mol for CO2
    :return c_ppm:      concentration in ppm (parts per million)
    """

    # molar volume of 24,471 if None is given
    if mol_vol is None:
        mol_vol = 24.471

    # Molar mass of CO2 if None is given
    if mol_mass is None:
        mol_mass = 44.01

    return c_mg_m3 * mol_vol / mol_mass
