from pythmath import square_root, power


def slope(x, y):
    """
    Calculates the slope of a line from x and y coordinates.

    Slope of Line: The slope of a line is defined as the change in y coordinate with respect to the change in x
    coordinate of that line. The net change in y coordinate is Δy, while the net change in the x coordinate is Δx.

    :param x: Value of x coordinates x1, x2 in a list.
    :param y: Value of y coordinates y1, y2 in a list.
    :return: Slope of a line from x and y coordinates.
    """
    if len(x) and len(y) == 2:
        x1 = x[0]
        x2 = x[-1]
        y1 = y[0]
        y2 = y[-1]
        return (y2 - y1) / (x2 - x1)
    else:
        return "List must contain [x1, x2] and [y1, y2] values."


def y_intercept(x, y):
    """
    Gets the y intercept from x and y coordinates.

    y intercept: The y-intercept is the point where the graph intersects the y-axis. To graph, any function that is
    of the form y = f(x) finding the intercepts is really important. There are two types of intercepts that a
    function can have. They are the x-intercept and the y-intercept. An intercept of a function is a point where the
    graph of the function cuts the axis.

    :param x: Value of x coordinates x1, x2 in a list
    :param y: Value of y coordinates y1, y2 in a list
    :return: y intercept from x and y coordinates.
    """
    x1 = x[0]
    y1 = y[0]
    s = slope(x, y)
    return y1 - s * x1


def midpoint(x, y):
    """
    Calculates the midpoint or middle point of a line from x and y coordinates

    Midpoint: In geometry, the midpoint is the middle point of a line segment. It is equidistant from both endpoints,
    and it is the centroid both of the segment and of the endpoints. It bisects the segment.

    :param x: Value of x coordinates x1, x2 in a list.
    :param y: Value of y coordinates y1, y2 in a list.
    :return: Midpoint or middle point of a line from x and y coordinates
    """
    x1 = x[0]
    y1 = y[0]
    x2 = x[-1]
    y2 = y[-1]
    midx = (x1 + x2) / 2
    midy = (y1 + y2) / 2
    return "({}, {})".format(midx, midy)


def line_dist(x, y):
    """
    Calculates the distance from a point to a line from x and y coordinates.

    Distance of a Line: In Euclidean geometry, the distance from a point to a line is the shortest distance from a
    given point to any point on an infinite straight line. It is the perpendicular distance of the point to the line,
    the length of the line segment which joins the point to nearest point on the line.

    :param x: Value of x coordinates x1, x2 in a list.
    :param y: Value of y coordinates y1, y2 in a list.
    :return: Distance from a point to a line from x and y coordinates.
    """
    x1 = x[0]
    y1 = y[0]
    x2 = x[-1]
    y2 = y[-1]
    return square_root((power(x2 - x1, 2)) + (power(y2 - y1, 2)))


def line_eqn(x, y):
    """
    Makes the equation of line from x and y coordinates.

    Formula: y = mx + c

    Equation of Line: The general equation of a straight line is y = mx + c, where m is the slope of the line and c
    is the y-intercept. It is the most common form of the equation of a straight line that is used in geometry. The
    equation of a straight line can be written in different forms such as point-slope form, slope-intercept form,
    general form, standard form, etc. A straight line is a two-dimensional geometrical entity that extends on both
    its ends till infinity.

    :param x: Value of x coordinates x1, x2 in a list
    :param y: Value of y coordinates y1, y2 in a list
    :return: equation of line from x and y coordinates.
    """
    m = slope(x, y)
    y_int = y_intercept(x, y)
    if y_int < 0:
        y_int = -y_int
        sign = '-'
    else:
        sign = '+'
    return 'y = {}x {} {}'.format(m, sign, y_int)
