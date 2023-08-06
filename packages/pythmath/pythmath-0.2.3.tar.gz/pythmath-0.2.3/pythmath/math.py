"""
An advance math library that performs math operations such as sine, cosine, tangent etc. and all the necessary
math functions

Finds area of square, area of rectangle, area of circle and area of triangle etc

Author: Roshaan Mehmood

GitHub: https://github.com/roshaan55/pythmath
"""
pi = 3.141592653589793
e = 2.718281828459045


def absolute(x):
    """
    Gets the absolute value of x, if negative it will be positive.

    :param x: Value of x to get its absolute value in positive.
    :return: Absolute value of x in positive
    """
    if x <= 0:
        return x * -1
    return x * 1


def power(a, b):
    """
    Calculates the power x**y (x to the power of y).

    :param a: Base number
    :param b: Exponent Number or power value
    :return: Return x**y (x to the power of y).
    """
    return float(pow(a, b))


def square_root(a):
    """
    Calculates the square root of a number

    :param a: Number Value
    :return: Square Root of a number to which the square root will be calculated
    """
    return float(a ** (1 / 2))


def nth_root(num, n):
    """
    Calculates the n under root or root of nth number.

    :param num: Number Value
    :param n: Value of n
    :return: n under root or root of nth number.
    """
    return float(num ** (1 / n))


def cube_root(a):
    """
    Calculates cube root of a number

    :param a: Number value to which the cube root will be calculated
    :return: Cube root of a number
    """
    return float(a ** (1 / 3))


def calc_lcm(a, b):
    """
    Calculate The Least Common Multiple of two numbers.

    :param a: First Number
    :param b: Second Number
    :return: The Least Common Multiple of two numbers
    """
    if a > b:
        greater = a
    else:
        greater = b

    while True:
        if (greater % a == 0) and (greater % b == 0):
            lcm = greater
            break
        greater += 1

    return float(lcm)


def calc_gcd(a, b):
    """
    Calculate the Greatest Common Divisor of two numbers.

    :param a: First Number
    :param b: Second Number
    :return: Greatest Common Divisor
    """
    if a > b:
        smaller = b
    else:
        smaller = a
    for i in range(1, smaller + 1):
        if (a % i == 0) and (b % i == 0):
            gcd = i
    return float(gcd)


def deg_to_rad(deg):
    """
    Convert angle x from degrees to radians.

    :param deg: angle in degrees.
    :return: Degrees to Radians.
    """
    return deg * pi / 180


def rad_to_deg(rad):
    """
    Convert angle x from radians to degrees.

    :param rad: angle in radians.
    :return: Radians to Degrees.
    """
    return rad * 180 / pi


def cos(x):
    """
    Calculates the cosine of x in radians.

    :param x: Value of x to be passed in cos(x) function.
    :return: Cosine of x in radians form.
    """
    return (e ** (x * 1j)).real


def cosd(x):
    """
    Calculates the cosine of x in degrees.

    :param x: Value of x to be passed in cosd(x) function.
    :return: Cosine of x in degrees form.
    """
    return cos(x * pi / 180)


def cot(x):
    """
    Calculates the cotangent of x in radians.

    :param x: Value of x to be passed in cot(x) function.
    :return: Cotangent of x in radians form.
    """
    return cos(x) / sin(x)


def cotd(x):
    """
    Calculates Cotangent of x in degrees.

    :param x: Value of x to be passed in cotd(x) function.
    :return: Cotangent of x in degrees form.
    """
    return cot(x * pi / 180)


def cosh(x):
    """
    Calculates the hyperbolic cosine of x in radians format.

    :param x: Value of x to be passed in cosh(x) function.
    :return: Hyperbolic cosine of x in radians format.
    """
    return (power(e, x) + power(e, -x)) / 2


def sin(x):
    """
    Calculates the sine of x in radians format.

    :param x: Value of x to be passed in sin(x) function.
    :return: Sine of x in radians.
    """
    return (e ** (x * 1j)).imag


def sind(x):
    """
    Calculates the sine of x in degrees format.

    :param x: Value of x to be passed in sind(x) function.
    :return: Sine of x in degrees.
    """
    return sin(x * pi / 180)


def sec(x):
    """
    Calculates the secant of x in radians format.

    :param x: Value of x to be passed in sec(x) function.
    :return: Secant of x in radians.
    """
    return 1 / cos(x)


def secd(x):
    """
    Calculates the secant of x in degrees format.

    :param x: Value of x to be passed in secd(x) function.
    :return: Secant of x in degrees.
    """
    return sec(x * pi / 180)


def cosec(x):
    """
    Calculates the cosecant of x in radians format.

    :param x: Value of x to be passed in cosec(x) function.
    :return: Cosecant of x in radians format.
    """
    return 1 / sin(x)


def cosecd(x):
    """
    Calculates the cosecant of x in degrees format.

    :param x: Value of x to be passed in cosecd(x) function.
    :return: Cosecant of x in degrees format.
    """
    return cosec(x * pi / 180)


def sinh(x):
    """
    Calculates the hyperbolic sine of x in radians format.

    :param x: Value of x to be passed in sinh(x) function.
    :return: Hyperbolic sine of x in radians.
    """
    return (power(e, x) - power(e, -x)) / 2


def tan(x):
    """
    Calculates the tangent of x in radians format.

    :param x: Value of x to be passed in tan(x) function.
    :return: Tangent of x in radians.
    """
    return sin(x) / cos(x)


def tand(x):
    """
    Calculates the tangent of x in degrees format.

    :param x: Value of x to be passed in tand(x) function.
    :return: Tangent of x in degrees.
    """
    return tan(x * pi / 180)


def tanh(x):
    """
    Calculates the hyperbolic tangent of x in radians format.

    :param x: Value of x to be passed in tanh(x) function.
    :return: Hyperbolic tangent of x in radians.
    """
    return sinh(x) / cosh(x)


def fact(num):
    """
    Find factorial of x.

    Raise a ValueError if x is negative or non-integral.

    :param num: Number of which you want to find it's factorial
    :return: Factorial of a number 'x'.
    """
    fact = 1
    if num < 0:
        raise ValueError("Sorry, factorial does not exist for negative numbers")
    if not isinstance(num, int):
        raise ValueError("Number is non integral")
    else:
        for i in range(1, num + 1):
            fact = fact * i
        return float(fact)


def isinteger(x):
    """
    Check whether the number is integral or non-integral.

    :param x: Number to check integral or non-integral.
    :return: True if number is integral otherwise False.
    """
    return isinstance(x, int)


def iseven(x):
    """
    Check whether the number is an even number.

    :param x: Number to check even or not.
    :return: True if number is even otherwise False.
    """
    if (x % 2) == 0:
        return True
    else:
        return False


def isodd(x):
    """
    Check whether the number is an odd number.

    :param x: Number to check odd or not.
    :return: True if number is odd otherwise False.
    """
    if (x % 2) != 0:
        return True
    else:
        return False


def isprime(x):
    """
    Check whether the number is a prime number.

    :param x: Number to check prime or not.
    :return: True if number is prime otherwise False.
    """
    if x > 1:
        for n in range(2, x):
            if (x % n) == 0:
                return False
        return True
    else:
        return False


def intsqrt(x):
    """
    Gets the integer part of square root from input.

    :param x: Number to calculate its square root.
    :return: Integer part of square root.
    """
    return floor(square_root(x))


def intcbrt(x):
    """
    Gets the integer part of cube root from input.

    :param x: Number to calculate its cube root.
    :return: Integer part of cube root.
    """
    return floor(cube_root(x))


def ispositive(x):
    """
    Checks whether the number is positive or not.

    :param x: Number to check positive or not.
    :return: True if number is positive otherwise False.
    """
    if x > 0:
        return True
    else:
        return False


def isnegative(x):
    """
    Checks whether the number is negative or not.

    :param x: Number to check negative or not.
    :return: True if number is negative otherwise False.
    """
    if x < 0:
        return True
    else:
        return False


def iszero(x):
    """
    Checks whether the number is zero or not.

    :param x: Number to check zero or not.
    :return: True if number is zero otherwise False.
    """
    if x == 0:
        return True
    else:
        return False


def is_sorted(lst):
    """
    Check whether the list is sorted or not.

    :param lst: List values to check is sorted or not
    :return: True if the list values are sorted otherwise False.
    """
    i = 1
    flag = 0
    while i < len(lst):
        if lst[i] < lst[i - 1]:
            flag = 1
        i += 1
    if not flag:
        return True
    else:
        return False


def floor(n):
    """
    Floors the number.

    :param n: Number you want to be floored.
    :return: Floor of the number
    """
    return int(n // 1)


def floatsum(numbers):
    """
    Calculates the accurate floating sum of values in a sequence or in list

    :param numbers: Numbers to calculate the floating sum
    :return: Accurate Floating Sum of numbers in a list
    """
    a = 0
    for num in numbers:
        a += num
    return float(a)


def floatabs(x):
    """
    Gets the absolute floating value of x.

    :param x: Number to get absolute floating value.
    :return: Absolute floating value of x.
    """
    return (x ** 2) ** 0.5


def ceil(n):
    """
    Find the ceiling of a number

    :param n: Number you want to be ceiled.
    :return: Ceiling of the number
    """
    return int(-1 * n // 1 * -1)


def remainder(num, divisor):
    """
    Find the remainder of two numbers.

    :param num: Number or Dividend
    :param divisor: Value of divisor
    :return: Remainder of two numbers.
    """
    return float(num - divisor * (num // divisor))


def euc_dist(x, y):
    """
    Finds the Euclidean Distance between two points x and y.

    :param x: First Point
    :param y: Second Point
    :return: Euclidean Distance between two points x and y.
    """
    return square_root(sum((px - py) ** 2 for px, py in zip(x, y)))


def exponential(x):
    """
    Finds the exponential of a specific number (e raised to the power of x).

    :param x: Number raise to the power of e
    :return: Exponential of a specific number (e raised to the power of x).
    """
    return power(e, x)


def percentage(val, total_val):
    """
    Calculates the percentage.

    :param val: Value
    :param total_val: Total Value
    :return: Percentage.
    """
    return val / total_val * 100


def sort(lst):
    """
    Sorts the elements in a list in ascending order.

    :param lst: List to be sorted.
    :return: Sorted List
    """
    if is_sorted(lst):
        # string = "The list is sorted already!"
        return "The list is sorted already!"
    else:
        a = []
        for i in range(len(lst)):
            a.append(min(lst))
            lst.remove(min(lst))
        return a


def count(lst):
    """
    Counts how many numbers in a list.

    :param lst: List to count the elements in it.
    :return: Count of numbers in a list.
    """
    c = 0
    for _ in lst:
        c += 1
    return c


def arr_sum(arr):
    """
    Calculates the sum of 1d array.

    :param arr: Array values of one dimension.
    :return: Sum of 1d array.
    """
    s = 0
    for i in arr:
        s = s + i
    return s


def arr_2d_sum(arr):
    """
    Calculates the sum of 2d array.

    :param arr: Values of 2d array.
    :return: Sum of 2d array.
    """
    my_sum = 0
    for row in arr:
        my_sum += sum(row)
    return my_sum


def nCr(n, r):
    """
    Calculates the combination nCr from n and r.

    :param n: Value of n
    :param r: Value of r
    :return: Result of nCr
    """
    return fact(n) // (fact(r) * fact(n - r))


def nPr(n, r):
    """
    Calculates the permutation nPr from n and r.

    :param n: Value of n
    :param r: Value of r
    :return: Result of nPr
    """
    return fact(n) / fact(n - r)


def minimum(lst):
    """
    Finds the minimum value in a list.

    :param lst: Values of list to find minimum value
    :return: Minimum value from a list.
    """
    return min(lst)


def maximum(lst):
    """
    Finds the maximum value in a list.

    :param lst: Values of list to find maximum value
    :return: Maximum value from a list.
    """
    return max(lst)


def fibonacci(first, second, n_terms=None):
    """
    Prints the fibonacci series in an empty list of n_terms

    Fibonacci Series: In mathematics, the Fibonacci numbers, commonly denoted Fₙ, form a sequence, the Fibonacci
    sequence, in which each number is the sum of the two preceding ones. The sequence commonly starts from 0 and 1,
    although some authors omit the initial terms and start the sequence from 1 and 1 or from 1 and 2.

    :param first: First Number
    :param second: Second Number
    :param n_terms: Number of terms to print fibonacci series, by default its value is 5
    :return: Returns the fibonacci series of n_terms
    """
    i = 2
    lst = [first, second]
    if n_terms is None:
        n_terms = 5
        while i < n_terms:
            fibo = first + second
            lst.append(fibo)
            first = second
            second = fibo
            i += 1
    else:
        while i < n_terms:
            fibo = first + second
            lst.append(fibo)
            first = second
            second = fibo
            i += 1
    return lst


def mult_two_lst(lst1, lst2):
    """
    Multiplies numbers of two list

    :param lst1: Numbers of list 1
    :param lst2: Numbers of list 2
    :return: Product list of numbers of list 1 and list 2
    """
    prod_lst = []
    for num1, num2 in zip(lst1, lst2):
        prod_lst.append(num1 * num2)
    return prod_lst


def multiply_lst(lst):
    """
    Multiplies numbers of a list.

    :param lst: List Values
    :return: Multiplication of numbers in a list.
    """
    result = 1
    for x in lst:
        result = result * x
    return result


def square_lst(lst):
    """
    Squares the numbers of a list

    :param lst: Numbers in a list
    :return: Squared list of numbers in a list
    """
    sq_lst = [number ** 2 for number in lst]
    return sq_lst


def pow_lst(lst, pow_val=2):
    """
    Calculates the power of each numbers in a list according to the user defined parameter power and appends
    the powered numbers in a new list.

    :param lst: Numbers in a list
    :param pow_val: Value of power to get the power of each number in a list, by default its value is 2
    :return: Powered list of each numbers of previous list.
    """
    sq_lst = [number ** pow_val for number in lst]
    return sq_lst


def isfloat(num):
    """
    Checks whether the number is float or not.

    :param num: Number to check float or not
    :return: True if the number is float otherwise False.
    """
    if isinstance(num, float):
        return True
    else:
        return False


def pos_neg(num):
    """ returns the positive number if the inputted number is negative and returns negative number if the inputted
    number is positive. """
    if ispositive(num):
        if isfloat(num):
            return float(num * - 1)
        else:
            return num * - 1
    elif isnegative(num):
        if isfloat(num):
            return float(num * - 1)
        else:
            return num * - 1


def prime_factors(num):
    """
    Gets the prime factors of a number, if a number is 100 it will get [2, 2, 5, 5].

    Prime Factors: prime factor is finding which prime numbers multiply together to make the original number.

    :param num: Value of num to calculate it's prime factors.
    :return: Prime factors of a number.
    """
    i = 2
    factors = []
    while i * i <= num:
        if num % i:
            i += 1
        else:
            num //= i
            factors.append(i)
    if num > 1:
        factors.append(num)
    return factors


def prime_numbers(s_range, end_range):
    """
    Generates a list of prime numbers from starting range to ending range.

    :param s_range: Starting Range
    :param end_range: Ending Range
    :return: List of prime numbers from starting range to ending range.
    """
    prime_list = []
    for num in range(s_range, end_range):
        prime = True
        for i in range(2, num):
            if num % i == 0:
                prime = False
        if prime:
            prime_list.append(num)
    return prime_list


def odd_numbers(s_range, end_range):
    """
    Generates a list of odd numbers from starting range to ending range.

    :param s_range: Starting Range
    :param end_range: Ending Range
    :return: List of odd numbers from starting range to ending range.
    """
    odd_list = []
    for num in range(s_range, end_range):
        odd = True
        for i in range(1, num):
            if num % 2 == 0:
                odd = False
        if odd:
            odd_list.append(num)
    return odd_list


def even_numbers(s_range, end_range):
    """
    Generates a list of even numbers from starting range to ending range.

    :param s_range: Starting Range
    :param end_range: Ending Range
    :return: List of even numbers from starting range to ending range.
    """
    odd_list = []
    for num in range(s_range, end_range):
        odd = True
        for i in range(1, num):
            if num % 2 != 0:
                odd = False
        if odd:
            odd_list.append(num)
    return odd_list


def quad_eqn(a, b, c):
    """
    Solves the quadratic equation and gets the roots of a quadratic equation.

    Quadratic Equation: In algebra, a quadratic equation is any equation that can be rearranged in standard form as
    where x represents an unknown, and a, b, and c represent known numbers, where a ≠ 0. If a = 0, then the equation
    is linear, not quadratic, as there is no ax^2 term.

    :param a: Value of a
    :param b: Value of b
    :param c: Value of c
    :return: Roots of a quadratic equation
    """
    discriminant = b ** 2 - 4 * a * c
    if discriminant >= 0:
        x_1 = (-b + square_root(discriminant)) / 2 * a
        x_2 = (-b - square_root(discriminant)) / 2 * a
    else:
        x_1 = complex((-b / (2 * a)), square_root(-discriminant) / (2 * a))
        x_2 = complex((-b / (2 * a)), -square_root(-discriminant) / (2 * a))

    if a == 0:
        return "Value of a is 0, thus the equation is not a quadratic equation."

    if discriminant > 0:
        return "The function has two distinct real roots: {} and {}".format(x_1, x_2)
    elif discriminant == 0:
        return "The function has one double root: {}".format(x_1)
    else:
        # print("The function has two complex (conjugate) roots: ", x_1, " and ", x_2)
        return "The function has two complex (conjugate) roots: {} and {}".format(x_1, x_2)


def num_factors(x):
    """
    Factorise a number 'x' and returns the list of factors.

    :param x: Value of x
    :return: List of factors of a number.
    """
    factors = []
    for i in range(1, x + 1):
        if x % i == 0:
            factors.append(i)
    return factors


def avg_rate_change(f_a, f_b, a, b):
    """
    Calculates the average rate of change from f(a) and f(b) calculated from a general function f(x).

    Average Rate of Change: The Average Rate of Change function is defined as the average rate at which one quantity
    is changing with respect to something else changing. In simple terms, an average rate of change function is a
    process that calculates the amount of change in one item divided by the corresponding amount of change in another.

    :param f_a: f(a) value from general f(x) function
    :param f_b: f(b) value from general f(x) function
    :param a: Value of a
    :param b: Value of b
    :return: Average rate of change from f(a) and f(b) calculated from a general function f(x).
    """
    return (f_b - f_a) / (b - a)
