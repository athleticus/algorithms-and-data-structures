import unittest
import peak_2d


class AbstractClasses:
    class AbstractTwoDPeakFinder(unittest.TestCase):
        @classmethod
        def setUpClass(cls):
            raise NotImplementedError()

        def test_basic(self):
            # Singleton
            self.assertEqual(self._method([[1]]), (0, 0))

        def test_top_left(self):
            A = [
                [7, 6, 5, 4],
                [6, 5, 4, 3],
                [5, 4, 3, 2],
                [4, 3, 2, 1]
            ]

            self.assertEqual(self._method(A), (0, 0))

        def test_bottom_left(self):
            A = [
                [7, 6, 5, 4],
                [6, 5, 4, 3],
                [5, 4, 3, 2],
                [4, 3, 2, 1]
            ]

            A.reverse()

            self.assertEqual(self._method(A), (3, 0))

        def test_top_right(self):
            A = [
                [7, 6, 5, 4],
                [6, 5, 4, 3],
                [5, 4, 3, 2],
                [4, 3, 2, 1]
            ]

            for row in A:
                row.reverse()

            self.assertEqual(self._method(A), (0, 3))

        def test_bottom_right(self):
            A = [
                [7, 6, 5, 4],
                [6, 5, 4, 3],
                [5, 4, 3, 2],
                [4, 3, 2, 1]
            ]

            for row in A:
                row.reverse()
            A.reverse()

            self.assertEqual(self._method(A), (3, 3))

        def test_multiple(self):
            A = [
                [1, 2, 5, 3, 4],
                [2, 7, 3, 2, 2],
                [9, 6, 8, 3, 2]
            ]

            self.assertIn(self._method(A),
                          {(1, 1), (0, 2), (0, 4), (2, 0), (2, 2)})


class TestBinarySearch(AbstractClasses.AbstractTwoDPeakFinder, unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls._method = staticmethod(peak_2d.find_2d_peak_linear_binary)


class TestGreedy(AbstractClasses.AbstractTwoDPeakFinder, unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls._method = staticmethod(peak_2d.find_2d_peak_greedy)


if __name__ == "__main__":
    unittest.main()
