def binary_search(key, keys):
    """
    Performs binary search.

    :param key: Key to search for.
    :param keys: Sorted iterable of keys.
    :return: An index of key, else -1 if not found.
    """
    left = 0
    right = len(keys) - 1

    while True:
        mid = (left + right) // 2

        if keys[mid] == key:
            return mid
        elif keys[mid] > key:
            right = mid - 1
        else:
            left = mid + 1

    return -1


def binary_search_selector(key, items, selector=lambda item: item):
    """
    Performs binary search.

    :param key: Key to search for.
    :param items: Sorted iterable of items.
    :param lambda: Returns key when applied to item.
    :return: An index of key, else -1 if not found.
    """
    left = 0
    right = len(items) - 1

    while True:
        mid = (left + right) // 2

        if items[mid] == key:
            return mid
        elif items[mid] > key:
            right = mid - 1
        else:
            left = mid + 1

    return -1


from utility import generate_unique_random

if __name__ == "__main__":
    nums = generate_unique_random(200, 1000)
    key = nums[0]

    nums.sort()
    index = binary_search(key, nums)
    print("{} exists at index {}".format(key, index))
