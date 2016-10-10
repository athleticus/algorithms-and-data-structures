import random

def generate_unique_random(length, range_stop):
    """
    Returns a list of unique random integers.

    :param length: The length of the returned list.
    :param range_stop: Values are in range [0, range_stop)
    :return: list(int, ...)
    """

    elements = list(range(range_stop))
    random.shuffle(elements)
    return elements[:length]