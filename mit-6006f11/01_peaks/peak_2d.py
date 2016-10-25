"""
A 2d-peak is defined on an MxN matrix A, such that:
a_{i-1, j} <= a_{i, j} >= a_{i+1, j}
and
a_{i, j-1} <= a_{i, j} >= a_{i, j+1}

Out of bounds comparisons are ignored, as with peak_1d.py

The proof that a peak exists is similar to that of peak_1d.py, but extended
to two dimensions.
"""

# E, S, W, N
DELTAS = [(0, 1), (1, 0), (0, -1), (-1, 0)]


def find_2d_peak_greedy(nums):
    """
    Finds a 2d-peak using a greedy ascent algorithm.

    Algorithm runs in O(mn), where m, n = len(nums), len(nums[0])

    From a starting position, the algorithm moves to a larger neighbour until
    it cannot proceed, at which point the current position is a peak.

    :param nums: The 2d-matrix A to search.
    :return: Index of 2d-peak.

    Raises:
        IndexError if either dimension is 0.
    """

    rows, columns = len(nums), len(nums[0])

    if rows == 0 or columns == 0:
        raise IndexError("Invalid dimensions {}x{}".format(rows, columns))

    i = rows // 2
    j = columns // 2

    while True:
        for di, dj in DELTAS:
            adj_i = i + di
            adj_j = j + dj

            # Ignore out of bounds
            if not (0 <= adj_i < rows and 0 <= adj_j < columns):
                continue

            # Move to adjacent, if not less than
            if nums[adj_i][adj_j] > nums[i][j]:
                i = adj_i
                j = adj_j
                break
        else:
            return i, j


def find_2d_peak_linear_binary(nums):
    """
    Finds a 2d-peak using a linear binary search.

    Algorithm runs in O(...

    :param nums: The 2d-matrix A to search.
    :return: Index of 2d-peak.

    Raises:
        IndexError if either dimension is 0.
    """

    rows, columns = len(nums), len(nums[0])

    if rows == 0 or columns == 0:
        raise IndexError("Invalid dimensions {}x{}".format(rows, columns))

    for i in range(rows):
        # Find global maximum in row
        row = nums[i]
        global_max = row[0]
        global_max_j = 0

        for j in range(1, len(row)):
            if row[j] > global_max:
                global_max = row[j]
                global_max_j = j

        # Detect 1d-peak in column
        j = global_max_j

        # (top row or > top adj) and (bottom row or > bottom adj.)
        if (i - 1 < 0 or nums[i - 1][j] <= nums[i][j]) and\
                (i + 1 >= rows or nums[i][j] >= nums[i + 1][j]):
            return i, j
