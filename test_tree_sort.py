import unittest
import random
from tree_sort import TreeSorter


class TestTreeSort(unittest.TestCase):
    
    def setUp(self):
        self.sorter = TreeSorter()
    
    def test_empty_array(self):
        """Пустой массив"""
        arr = []
        result = self.sorter.sort(arr)
        self.assertEqual(result, [])
    
    def test_single_element(self):
        """Один элемент"""
        arr = [42]
        result = self.sorter.sort(arr)
        self.assertEqual(result, [42])
    
    def test_sorted_array(self):
        """Отсортированный массив"""
        arr = [1, 2, 3, 4, 5, 6, 7, 8, 9, 10]
        result = self.sorter.sort(arr)
        self.assertEqual(result, [1, 2, 3, 4, 5, 6, 7, 8, 9, 10])
    
    def test_reverse_sorted(self):
        """Обратный порядок"""
        arr = [10, 9, 8, 7, 6, 5, 4, 3, 2, 1]
        expected = [1, 2, 3, 4, 5, 6, 7, 8, 9, 10]
        result = self.sorter.sort(arr)
        self.assertEqual(result, expected)
    
    def test_random_array(self):
        """Случайный массив"""
        arr = [5, 2, 8, 1, 9, 3, 7, 4, 6]
        expected = [1, 2, 3, 4, 5, 6, 7, 8, 9]
        result = self.sorter.sort(arr)
        self.assertEqual(result, expected)
    
    def test_duplicates(self):
        """Дубликаты"""
        arr = [3, 1, 4, 1, 5, 9, 2, 6, 5, 3, 5]
        expected = [1, 1, 2, 3, 3, 4, 5, 5, 5, 6, 9]
        result = self.sorter.sort(arr)
        self.assertEqual(result, expected)
    
    def test_negative_numbers(self):
        """Отрицательные числа"""
        arr = [-5, 10, -3, 0, 8, -1, 2]
        expected = [-5, -3, -1, 0, 2, 8, 10]
        result = self.sorter.sort(arr)
        self.assertEqual(result, expected)


def run_tests():
    """Запуск всех тестов"""
    suite = unittest.TestLoader().loadTestsFromTestCase(TestTreeSort)
    runner = unittest.TextTestRunner(verbosity=2)
    result = runner.run(suite)
    
    print(f"\nРезультаты: {result.testsRun} тестов, "
          f"успешно: {result.testsRun - len(result.failures) - len(result.errors)}, "
          f"ошибок: {len(result.failures) + len(result.errors)}")
    
    return result


if __name__ == "__main__":
    run_tests()
