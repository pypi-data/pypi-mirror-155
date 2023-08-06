from pythmath import square_root, maximum, minimum, multiply_lst


def stdev(data):
    """
    Calculates the standard deviation from given dataset.

    Standard Deviation: In statistics, the standard deviation is a measure of the amount of variation or dispersion
    of a set of values. A low standard deviation indicates that the values tend to be close to the mean of the set,
    while a high standard deviation indicates that the values are spread out over a wider range.

    :param data: Values of given dataset
    :return: The standard deviation from given dataset.
    """
    get_mean = mean(data)
    s = 0
    for i in data:
        s += (i - get_mean) ** 2
    return square_root(s / (len(data) - 1))


def pstdev(data):
    """
    Calculates the standard deviation of population from given dataset.

    :param data: Values of given dataset
    :return: Standard deviation of population from given dataset
    """
    m = sum(data) / len(data)
    s = 0
    for i in data:
        s += (i - m) ** 2
    return square_root(s / (len(data)))


def mean_abs_dev(data):
    """
    Calculates the mean absolute deviation from given dataset.

    Mean Absolute Deviation: The mean absolute deviation (MAD) is a measure of variability that indicates the
    average distance between observations and their mean. MAD uses the original units of the data, which simplifies
    interpretation. Larger values signify that the data points spread out further from the average. Conversely,
    lower values correspond to data points bunching closer to it. The mean absolute deviation is also known as the
    mean deviation and average absolute deviation.

    :param data: Values of given dataset
    :return: Mean Absolute Deviation from given dataset
    """
    m = sum(data) / len(data)
    s = 0
    for i in range(len(data)):
        dev = abs(data[i] - m)
        s = s + round(dev, 2)
    return s / len(data)


def zscore(x, mean_val, st_dev):
    """
    Calculates the z score value from x, mean value and from value of standard deviation.

    Z Score: In statistics, the standard score is the number of standard deviations by which the value of a raw score
    is above or below the mean value of what is being observed or measured. Raw scores above the mean have positive
    standard scores, while those below the mean have negative standard scores.

    :param x: Standardized random variable
    :param mean_val: Mean Value
    :param st_dev: Value of standard deviation
    :return: z score value from x, mean value and from value of standard deviation.
    """
    return (x - mean_val) / st_dev


def stderr(data):
    """
    Calculates the standard error from given dataset.

    Standard Error: The standard error of a statistic is the standard deviation of its sampling distribution or an
    estimate of that standard deviation. If the statistic is the sample mean, it is called the standard error of the
    mean.

    :param data: Values of given dataset
    :return: Standard error from given dataset
    """
    return stdev(data) / square_root(len(data))


def samp_err(n, pst_dev, conf=1.96):
    """
    Calculates the sampling error.

    Sampling Error: In statistics, sampling errors are incurred when the statistical characteristics of a population
    are estimated from a subset, or sample, of that population.

    :param n: Size of sampling
    :param pst_dev: Value of standard deviation of population
    :param conf: Confidence level approx: 1.96
    :return: Sampling Error
    """
    return pst_dev / square_root(n) * conf


def variance(data, v_mode="std"):
    """
    Calculates the variance from given datasets or list.

    Variance: In probability theory and statistics, variance is the expectation of the squared deviation of a random
    variable from its population mean or sample mean. Variance is a measure of dispersion, meaning it is a measure of
    how far a set of numbers is spread out from their average value.

    :param data: Values of given dataset or a list
    :param v_mode: Mode of variance either standard(std) or population(popul).
    :return: Variance from given datasets or list.
    """
    m = mean(data)
    if v_mode == "std":
        return sum([(xi - m) ** 2 for xi in data]) / (len(data) - 1)
    elif v_mode == "pop":
        return sum([(xi - m) ** 2 for xi in data]) / (len(data))


def covariance(x, y, cov_mode="samp"):
    """
    Calculates the covariance from two datasets or lists of numbers x and y.

    Covariance: In probability theory and statistics, covariance is a measure of the joint variability of two random
    variables. If the greater values of one variable mainly correspond with the greater values of the other variable,
    and the same holds for the lesser values, the covariance is positive.

    :param x: Values of datas in x dataset
    :param y: Values of datas in y dataset
    :param cov_mode: Mode of covariance either sample or population, by default it is sample
    :return: Covariance from two datasets or lists of numbers x and y
    """
    if cov_mode == "samp":
        return sum([(xi - mean(x)) * (yi - mean(y)) for xi, yi in zip(x, y)]) / (len(x) - 1)
    elif cov_mode == "pop":
        return sum([(xi - mean(x)) * (yi - mean(y)) for xi, yi in zip(x, y)]) / (len(x))


def stats_range(data):
    """
    Calculates the statistical range from given dataset or set of integer values.

    Statistical Range: In statistics, the range of a set of data is the difference between the largest and smallest
    values. Difference here is specific, the range of a set of data is the result of subtracting the sample maximum
    and minimum. However, in descriptive statistics, this concept of range has a more complex meaning.

    :param data: Values of given dataset or set of integer values
    :return: Range from given dataset or set of integer values
    """
    return maximum(data) - minimum(data)


def midrange(data):
    """
    Calculates the midpoint range from given dataset or set of integer values.

    Midpoint Range: In statistics, the mid-range or mid-extreme is a measure of central tendency of a sample defined
    as the arithmetic mean of the maximum and minimum values of the data set.

    :param data: Values of given dataset or set of integer values
    :return: Midpoint range from given dataset or set of integer values
    """
    return (maximum(data) + minimum(data)) / 2


def mean(nums):
    """
    Calculates the exact arithmatic mean(average) of numbers in a list.

    :param nums: Numbers in a list to calculate their arithmatic mean(average).
    :return: Arithmatic mean(average) of numbers in a list.
    """
    return sum(nums) / len(nums)


def float_mean(nums):
    """
    Calculates the floating exact arithmatic mean(average) of numbers in a list.

    :param nums: Numbers in a list to calculate their arithmatic mean(average).
    :return: Floating arithmatic mean(average) of numbers in a list.
    """
    return float(sum(nums) / len(nums))


def harmonic_mean(data):
    """
    Calculates the harmonic mean from given dataset, list of numbers or tuple of numbers.

    Harmonic Mean: In mathematics, the harmonic mean is one of several kinds of average, and in particular,
    one of the Pythagorean means. It is sometimes appropriate for situations when the average rate is desired.

    :param data: Values of a given dataset, list of values or tuple of numbers.
    :return: Harmonic mean from given dataset, list of numbers or tuple of numbers.
    """
    s = 0
    for ele in data:
        s += 1 / ele
    return len(data) / s


def geometric_mean(data):
    """
    Calculates the geometric mean from given dataset, list of numbers or tuple of numbers.

    Geometric Mean: In statistics, the geometric mean is calculated by raising the product of a series of numbers to
    the inverse of the total length of the series. The geometric mean is most useful when numbers in the series are
    not independent of each other or if numbers tend to make large fluctuations.

    :param data: values of a given dataset, list of numbers or tuple of numbers
    :return: Geometric mean from given dataset, list of numbers or tuple of numbers.
    """
    num_prod = multiply_lst(data)
    n = len(data)
    return float(num_prod ** (1 / n))


def median(nums):
    """
    Calculates the median of numbers in a list.

    :param nums: Numbers in a list to calculate their median.
    :return: Median of numbers in a list.
    """
    n = len(nums)
    if n % 2 == 0:
        return nums[n // 2] + nums[n // 2 - 1] / 2
    else:
        return nums[n // 2]


def median_abs_dev(data):
    """
    Calculates the median absolute deviation from a given dataset, list of numbers or tuple of numbers.

    Median Absolute Deviation: In statistics, the median absolute deviation is a robust measure of the variability of
    a univariate sample of quantitative data. It can also refer to the population parameter that is estimated by the
    MAD calculated from a sample.

    :param data: Values of given dataset, list of numbers or tuples of numbers.
    :return: Median absolute deviation from a given dataset, list of numbers or tuple of numbers
    """
    med = median(data)
    deviations = sorted(abs(xi - med) for xi in data)
    return float(median(deviations))


def mode(nums):
    """
    Gets the mode of numbers in a list.

    :param nums: Numbers to get the mode of numbers in a list.
    :return: Mode of numbers in list.
    """
    unique_nums = list(set(nums))
    dictionary = {}
    for i in unique_nums:
        get_count = nums.count(i)
        dictionary[i] = get_count
    max_repeat = 0
    for i in unique_nums:
        get_value = dictionary[i]
        if get_value > max_repeat:
            max_repeat = get_value
    result = ''
    for i in unique_nums:
        if dictionary[i] == max_repeat:
            result = result + str(i) + " "
    return result
