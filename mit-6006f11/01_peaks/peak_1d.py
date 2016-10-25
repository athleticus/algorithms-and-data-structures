"""
A peak of A is defined as a_i, iff a_{i-1} <= a_i >= a{i+1}.
Comparison with previous term is ignored if a_i is the first term; similarly
for the last term.

A peak must exist, according to the following theorem:

    Assume a peak does not exist.

    If a_0 >= a_1, then a_0 would be a peak. Hence, a_1 > a_0.
    Similarly, a_2 > a_1, and in general a_{i+1} > a_{i} for all i < n - 1.
    But when i = n-2 (i.e. a_i is the second-last element), a_{i+1} must be
    greater than it, which means that the last element is a peak by
    definition.

    This is a contradiction, so the assumption that a peak does not exist is
    false. Therefore, there must exist a peak.
"""

def find_1d_peak_naive(nums):
    """
    Returns the index of a peak using a naive linear search.

    Algorithm runs in O(n), where n = len(nums).

    :param nums: List of numbers, A, to search.
    :return: Index of the peak.

    Raises:
        IndexError: If length is 0.
    """

    if len(nums) == 0:
        raise IndexError("Cannot search empty list.")

    # Singleton
    if len(nums) == 1:
        return 0

    # Check first
    if nums[0] >= nums[1]:
        return 0

    # Check second to second last
    for i in range(1, len(nums) - 1):
        if nums[i - 1] <= nums[i] >= nums[i + 1]:
            return i

    # Check last
    if nums[-1] >= nums[-2]:
        return len(nums) - 1


def find_1d_peak_binary(nums):
    """
    Returns the index of a peak using binary search.

    Algorithm runs in O(log n), where n = len(nums).

    :param nums: List of numbers, A, to search.
    :return: Index of the peak.

    Raises:
        IndexError: If length is 0.
    """

    if len(nums) == 0:
        raise IndexError("Cannot search empty list.")

    left = 0
    right = len(nums) - 1

    while True:
        if left >= right - 1:
            if nums[left] >= nums[right]:
                return left
            else:
                return right

        mid = (left + right) // 2

        if nums[mid] < nums[mid - 1]:  # go left for a peak
            right = mid
        elif nums[mid] < nums[mid + 1]:  # go right for a peak
            left = mid
        else:
            return mid
