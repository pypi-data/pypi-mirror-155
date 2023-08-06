from pythmath.math import square_root, power, pi


def volume_cone(r, h):
    """
    Calculates the volume of a cone from values of radius and height.

    :param r: Values of radius of cone
    :param h: Value of height of cone
    :return: Volume of a cone from values of radius and height
    """
    return pi * power(r, 2) * h / 3


def surf_area_cube(a):
    """
    Calculates the surface area of a cube.

    :param a: Value of a
    :return: Surface area of a cube.
    """
    return 6 * power(a, 2)


def volume_cube(a):
    """
    Calculates the volume of a cube.

    :param a: Value of a
    :return: Volume of a cube
    """
    return power(a, 3)


def surf_area_cuboid(l, b, h):
    """
    Calculates the surface area of a cuboid from values of length, base and height.

    :param l: Value of Length of cuboid
    :param b: Value of base of cuboid
    :param h: Value of height of cuboid
    :return: Surface area of a cuboid from values of length, base and height.
    """
    return 2 * (l * b + b * h + h * l)


def volume_cuboid(l, b, h):
    """
    Calculates the volume of a cuboid from values of length, base and height.

    :param l: Value of Length of cuboid
    :param b: Value of base of cuboid
    :param h: Value of height of cuboid
    :return: Volume of a cuboid from values of length, base and height.
    """
    return l * b * h


def area_circle(r):
    """
    Calculate the area of circle from given radius.

    :param r: Radius of a circle.
    :return: Area of a circle.
    """
    return float(pi * power(r, 2))


def circle_circum(r):
    """
    Calculates the circumference of a circle from given radius

    :param r: Value of radius
    :return: Circumference of a circle from given radius
    """
    return 2 * pi * r


def surf_area_cylinder(r, h):
    """
    Calculates the surface area of a cylinder from values of radius and height.

    :param r: Value of radius of cylinder
    :param h: Value of height of cylinder
    :return: Surface area of a cylinder from values of length, base and height.
    """
    return 2 * pi * r * (r + h)


def volume_cylinder(r, h):
    """
    Calculates the volume of a cylinder from values of radius and height.

    :param r: Value of radius of cylinder
    :param h: Value of height of cylinder
    :return: Volume of a cylinder from values of radius and height
    """
    return pi * power(r, 2) * h


def area_rect(a, b):
    """
    Calculates the area of rectangle from given points or sides.

    :param a: Side 'a' of a rectangle.
    :param b: Side 'b' of a rectangle.
    :return: Area of a rectangle.
    """
    return float(a * b)


def perimeter_rect(a, b):
    """
    Calculates the perimeter of a rectangle from given points or sides.

    :param a: Side 'a' of a rectangle.
    :param b: Side 'b' of a rectangle.
    :return: Area of a rectangle.
    """
    return float(2 * (a + b))


def area_square(side):
    """
    Calculates the area of a square from given side, a square has four equal sides,
    therefore it takes only one side to calculate its area.

    :param side: Side of a square.
    :return: Area of a square
    """
    return float(side * side)


def perimeter_square(a):
    """
    Calculates the perimeter of square from a side of square

    :param a: Value of one side of a square
    :return: Perimeter of square from a side of square
    """
    return 4 * a


def surf_area_sphere(r):
    """
    Calculates the surface area of sphere from value of radius.

    :param r: Value of radius of sphere
    :return: Surface area of sphere from value of radius
    """
    return 4 * pi * power(r, 2)


def volume_sphere(r):
    """
    Calculates the volume of a sphere from value of radius.

    :param r: Value of radius of sphere
    :return: Volume of a sphere from value of radius
    """
    return 4 / 3 * pi * power(r, 3)


def perimeter_parallelo(a, b):
    """
    Calculates the perimeter of a parallelogram.

    :param a: Value of a
    :param b: Value of b
    :return: Perimeter of a parallelogram
    """
    return 2 * (a + b)


def area_parallelo(b, h):
    """
    Calculates the area of a parallelogram.

    :param h: height of parallelogram
    :param b: base of parallelogram
    :return: Area of a parallelogram
    """
    return b * h


def area_trapezoid(a, b, h):
    """
    Calculates the area of trapezoid.

    :param a: Value of a base
    :param b: Value of b base
    :param h: Value of height
    :return: Area of trapezoid.
    """
    return (a + b) / 2 * h


def area_triangle(a, b, c):
    """
    Calculates the area of a triangle from three sides of a triangle.

    :param a: First side of a triangle.
    :param b: Second side of a triangle.
    :param c: Third side of a triangle.
    :return: Area of a triangle.
    """
    s = (a + b + c) / 2
    return square_root((s * (s - a) * (s - b) * (s - c)))


def p_right_triangle(a, b):
    """
    Calculates the perimeter of a right angle triangle.

    :param a: Value of a
    :param b: Value of b
    :return: Perimeter of a right angle triangle
    """
    return a + b + hypotenuse(a, b)


def perimeter_triangle(a, b, c):
    """
    Calculates the perimeter of a triangle

    :param a: Value of a
    :param b: Value of b
    :param c: Value of c
    :return: perimeter of a triangle
    """
    return a + b + c


def hypotenuse(x, y):
    """
    Calculates the hypotenuse of x and y

    :param x: Value of x
    :param y: Value of y
    :return: Hypotenuse of x and y
    """
    return square_root(x ** 2 + y ** 2)


def angle(arc_len, r):
    """
    Calculates the angle from arc length and radius, it basically uses central angle formula.

    Arc Length: Arc length is the distance between two points along a section of a curve. Determining the length of
    an irregular arc segment by approximating the arc segment as connected line segments is also called rectification
    of a curve.

    :param arc_len: Value of arc length
    :param r: Value of radius.
    :return: Value of angle from arc length and radius
    """
    return arc_len * 360 / (2 * pi * r)


def arc_length(a, r):
    """
    Calculates the arc length from angle (in radians) and radius.

    Arc Length: Arc length is the distance between two points along a section of a curve. Determining the length of
    an irregular arc segment by approximating the arc segment as connected line segments is also called rectification
    of a curve.

    :param a: Value of angle in radians.
    :param r: Value of radius.
    :return: Value of arc length
    """
    return a * r


def arc_length_deg(a, r):
    """
    Calculates the arc length from angle (in degrees) and radius.

    Arc Length: Arc length is the distance between two points along a section of a curve. Determining the length of
    an irregular arc segment by approximating the arc segment as connected line segments is also called rectification
    of a curve.

    :param a: Value of angle in degrees.
    :param r: Value of radius.
    :return: Value of arc length
    """
    return 2 * pi * r * a / 360
