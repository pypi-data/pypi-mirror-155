"""
An advance math module that performs math operations and all the necessary math functions such as absolute, mean,
median, mode, factorial, sin, cos, tan etc

It Includes fractions to solve and simplify the fractions.

Pure math module which has no external modules(math, numpy and sympy etc.) imported.

Author: Roshaan Mehmood

GitHub: https://github.com/roshaan55/pythmath
"""
from pythmath.math import absolute, power, square_root, cube_root, nth_root, calc_lcm, calc_gcd, deg_to_rad, \
    rad_to_deg, cos, cosd, cot, cotd, cosh, cosec, cosecd, sin, sind, sec, secd, sinh, tan, tand, tanh, fact, \
    isinteger, iseven, isodd, isprime, intsqrt, intcbrt, ispositive, isnegative, iszero, floor, ceil, \
    floatsum, floatabs, remainder, euc_dist, exponential, is_sorted, percentage, sort, count, arr_sum, arr_2d_sum, \
    nCr, nPr, minimum, maximum, fibonacci, mult_two_lst, multiply_lst, square_lst, pow_lst, \
    isfloat, pos_neg, prime_factors, prime_numbers, odd_numbers, even_numbers, quad_eqn, num_factors, avg_rate_change
from pythmath.fractions import fraction, frac_to_float, float_to_frac
from pythmath.geometry import volume_cone, surf_area_cube, volume_cube, surf_area_cuboid, volume_cuboid, area_rect, \
    area_square, perimeter_square, surf_area_sphere, volume_sphere, perimeter_parallelo, area_parallelo, area_circle, \
    circle_circum, surf_area_cylinder, volume_cylinder, area_trapezoid, area_triangle, p_right_triangle, \
    perimeter_triangle, perimeter_rect, hypotenuse, arc_length, arc_length_deg, angle
from pythmath.statistics import stdev, pstdev, mean_abs_dev, zscore, stderr, samp_err, variance, covariance, \
    stats_range, midrange, mean, float_mean, harmonic_mean, geometric_mean, median, median_abs_dev, mode
from pythmath.errors import perc_error, abs_error, rel_error
from pythmath.lines import slope, line_dist, line_eqn, midpoint, y_intercept
