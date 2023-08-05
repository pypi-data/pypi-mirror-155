""" Physical measurement units conversation module for Python 3.
"""
import numpy as np

G_ACCEL = 9.80665
_prefix = {'': 1,
           'd': 1e1,
           'c': 1e2,
           'm': 1e3,
           'μ': 1e6,
           'n': 1e9,
           'p': 1e12,
           'f': 1e15,
           'a': 1e18,
           'z': 1e21,
           'y': 1e24,
           'da': 1e-1,
           'h': 1e-2,
           'k': 1e-3,
           'M': 1e-6,
           'G': 1e-9,
           'T': 1e-12,
           'P': 1e-15,
           'E': 1e-18,
           'Z': 1e-21,
           'Y': 1e-24}
length_dict = {**{i + 'm': _prefix[i] for i in _prefix},
               'ft': 3.28084,
               'in': 39.37008,
               'NM': 5.399565e-4,
               'mi': 6.213712e-4}
mass_dict = {**{i + 'g': _prefix[i] * 1e3 for i in _prefix},
             't': 1e-3,
             'lb': 2.204623,
             'oz': 35.27396}
time_dict = {'s': 1,
             'min': 1/60,
             'h': 1/3600}
acceleration_dict = {'m/s²': 1,
                     'ft/s²': length_dict['ft']}
angle_dict = {'rad': 1,
              'deg': np.pi/180}
area_dict = {**{i+'²': length_dict[i]**2 for i in length_dict},
             'ha': 1e-4,
             'a': 1e-2}
density_dict = {'kg/m³': 1,
                'g/cm³': mass_dict['g']/length_dict['cm']**3,
                'lb/in³': mass_dict['lb']/length_dict['in']**3,
                'lb/ft³': mass_dict['lb']/length_dict['ft']**3}
inertia_dict = {'kg·m²': 1,
                'lb·ft²': mass_dict['lb']/length_dict['ft']**3}
force_dict = {'N': 1,
              'kN': 1e-3,
              'lbf': mass_dict['lb']/G_ACCEL}
pressure_dict = {**{i + 'Pa': _prefix[i] for i in _prefix},
                 'psi': 1.450377e-4,
                 'kpsi': 1.450377e-7,
                 'bar': 1e-5,
                 'atm': 9.869233e-6,
                 'mmHg': 7.500638e-3,
                 'lbf/ft²': force_dict['lbf']/length_dict['ft']**2}
power_dict = {**{i + 'W': _prefix[i] for i in _prefix},
              'HP': 0.001341022}
second_moment_area_dict = {i+'⁴': length_dict[i]**4 for i in length_dict}
speed_dict = {'m/s': 1,
              'km/h': length_dict['km']/time_dict['h'],
              'kt': length_dict['NM']/time_dict['h']}
volume_dict = {**{i+'³': length_dict[i]**3 for i in length_dict},
               **{i+'l': _prefix[i]**3 * 1e3 for i in _prefix},
               'gal': 264.172}


si_dicts = [acceleration_dict,
            angle_dict,
            area_dict,
            density_dict,
            force_dict,
            inertia_dict,
            length_dict,
            mass_dict,
            power_dict,
            pressure_dict,
            second_moment_area_dict,
            speed_dict,
            volume_dict]


def unit_conversion(value, from_unit=None, to_unit=None):
    """ Measurement units conversion.

    Using this function, `value` `from_unit` is converted to
    `new_value` `to_unit`. If one of the units is not provided, it is assumed
    to be an SI unit. If no units are provided, the same value is returned.

    Args:
        value (float, list, str or numpy.array): Value(s) to be converted. If
            given as a string, a unit can be specified.
        from_unit (str, optional): Unit of the input value(s).
        to_unit (str, optional): Unit the value(s) are converted to.

    Returns:
        float or numpy.ndarray: Converted value(s).

    Raises:
        ValueError: If given units are inconsistent, unknown or not compatible.
        NotImplementedError: Not implemented features.

    """
    if isinstance(value, (list)):
        value = np.array(value)
    elif isinstance(value, (str)):
        i_value, i_unit = value.split()
        if from_unit is not None and i_unit != from_unit:
            raise ValueError('Inconsistent units.')
        value = float(i_value)
        from_unit = i_unit

    if isinstance(value, (list, np.ndarray)):
        if isinstance(value[0], (str)):
            raise NotImplementedError('Conversion of a list of strings not yet'
                                      + ' implemented.')

    #
    if from_unit is None and to_unit is None:
        # If no units are provided, return same value
        return value

    if to_unit is None:
        # If only from_unit is provided, convert to SI units
        for dict_i in si_dicts:
            if from_unit in dict_i.keys():
                return value/dict_i[from_unit]
        raise ValueError(f"Unknown unit {from_unit}.")

    if from_unit is None:
        # If only to_unit is provided, assume that the input is given in SI
        # units
        for dict_i in si_dicts:
            if to_unit in dict_i.keys():
                return value*dict_i[to_unit]
        raise ValueError(f"Unknown unit {from_unit}.")

    # Check if from_unit and to_unit are in the same dict
    # and use it to calculate the new value
    for dict_i in si_dicts:
        if from_unit in dict_i.keys() and to_unit in dict_i.keys():
            return value*dict_i[to_unit]/dict_i[from_unit]
    raise ValueError(f'Units {from_unit} and {to_unit}' +
                     ' are not compatible.')
