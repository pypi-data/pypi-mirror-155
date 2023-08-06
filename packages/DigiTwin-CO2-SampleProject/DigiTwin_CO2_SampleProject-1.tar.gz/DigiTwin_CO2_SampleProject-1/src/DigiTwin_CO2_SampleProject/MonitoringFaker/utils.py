import numpy as np

def static_value_fcn(value):

    def static(*args, **kwargs):
        return value

    return static


def sinus_value_fcn(shift=0, amp=1, freq=1, phase_shift=0):
    """
    Creates a function which returns the sinus for time:
    return shift + amp * np.sin(omega * time + phase_shift)
    :param shift:
    :param amp:
    :param freq:
    :param phase_shift:
    :return: function which returns the sinus for time
    """
    def sinus_fcn(time, *args, **kwargs):

        omega = 2 * np.pi * freq

        return shift + amp * np.sin(omega * time + phase_shift)

    return sinus_fcn


def sinus_int_value_fcn(shift=0, amp=1, freq=1, phase_shift=0):
    """
    Creates a function which returns the sinus for time:
    return shift + amp * np.sin(omega * time + phase_shift)
    :param shift:
    :param amp:
    :param freq:
    :param phase_shift:
    :return: function which returns the sinus for time
    """
    def sinus_fcn(time, *args, **kwargs):

        omega = 2 * np.pi * freq

        return round(shift + amp * np.sin(omega * time + phase_shift))

    return sinus_fcn


def cosinus_value_fcn(shift=0, amp=1, freq=1, phase_shift=0):
    """
    Creates a function which returns the sinus for time:
    return shift + amp * np.sin(omega * time + phase_shift)
    :param shift:
    :param amp:
    :param freq:
    :param phase_shift:
    :return: function which returns the sinus for time
    """
    def cosinus_fcn(time, *args, **kwargs):

        omega = 2 * np.pi * freq

        return shift + amp * np.sin(omega * time + phase_shift)

    return cosinus_fcn


def random_range_value_fcn(min, max, val_type=float):

    def rand_range(*args, **kwargs):
        return np.random.uniform(low=min, high=max)

    return rand_range
