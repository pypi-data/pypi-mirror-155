from pythmath import absolute


def perc_error(measured_val, true_val):
    """
    Calculates the percentage error from measured value and true or real value.

    :param measured_val: Measured Value
    :param true_val: True or real value
    :return: Percentage error from measured value and true or real value.
    """
    return absolute((measured_val - true_val)) / true_val * 100


def abs_error(measured_val, true_val):
    """
    Calculates the absolute error from measured value and true or real value.

    :param measured_val: Measured value.
    :param true_val: True or real value
    :return: Absolute error from measured values and true or real value.
    """
    return absolute(measured_val - true_val)


def rel_error(measured_val, true_val):
    """
    Calculates the relative error from measured value and true or real value.

    :param measured_val: Measured Value
    :param true_val: True or real value
    :return: Relative error from measured value and true or real value.
    """
    return abs_error(measured_val, true_val) / true_val
