import unittest
from Statistics import Statistics

class UpdateStats_tests(unittest.TestCase):
    def test_first(self):
        stats = {
            'a': 1,
            'b': 2,
            '3': 174
        }
        statistics = Statistics('../Data/vacancies.csv', '')
        statistics.update_stats('a', 2, stats)
        self.assertEqual(stats['a'], 3)

    def test_second(self):
        stats = {
            'a': 1,
            'b': 2,
            '3': 174
        }
        statistics = Statistics('../Data/vacancies.csv', '')
        statistics.update_stats('d', 2, stats)
        self.assertEqual(stats['d'], 2)

if __name__ == '__main__':
    unittest.main()