import unittest
import peak_1d

class AbstractClasses:
    class AbstractOneDPeakFinder(unittest.TestCase):
        @classmethod
        def setUpClass(cls):
            raise NotImplementedError()

        def test_basic(self):
            # Singleton
            self.assertEqual(self._method([1]), 0)

        def test_first_and_last(self):
            self.assertEqual(self._method([1, 2, 3, 4, 5, 6]), 5)
            self.assertEqual(self._method([6, 5, 4, 3, 2, 1]), 0)

        def test_second_and_second_last(self):
            self.assertEqual(self._method([1, 2, 3, 4, 6, 5]), 4)
            self.assertEqual(self._method([5, 6, 4, 3, 2, 1]), 1)

        def test_single_mixed(self):
            self.assertEqual(self._method([1, 2, 3, 4, 5, 6, 5, 4, 3, 2, 1]), 5)

        def test_multi_mixed(self):
            self.assertIn(self._method([20, 1, 5, 2, 6, 9, 1, 10]), {0, 2, 5, 7})


class TestBinarySearch(AbstractClasses.AbstractOneDPeakFinder, unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls._method = staticmethod(peak_1d.find_1d_peak_binary)


class TestNaive(AbstractClasses.AbstractOneDPeakFinder, unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls._method = staticmethod(peak_1d.find_1d_peak_naive)


if __name__ == "__main__":
    unittest.main()
