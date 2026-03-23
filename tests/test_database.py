
import sys
import os
import time
import random

# Добавляем путь к родительской папке
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from database import (
    init_db, save_array, get_all_arrays_for_test, 
    clear_all_arrays_for_test, get_arrays_count_for_test,
    TEST_DB_PATH
)
from tree_sort import tree_sort_with_stats, is_sorted


class TestDatabase:
    """Класс для тестирования базы данных"""
    
    def __init__(self):
        self.test_db_path = TEST_DB_PATH
        self.results = []
    
    def generate_random_array(self, size: int) -> list:
        """Генерирует случайный массив"""
        return [random.randint(-100, 100) for _ in range(size)]
    
    def test_add_arrays(self, count: int, array_size_range=(5, 20)) -> dict:
        """
        Тест добавления массивов в базу данных
        """
        print(f"\n{'='*60}")
        print(f"ТЕСТ: Добавление {count} массивов")
        print(f"{'='*60}")
        
        # Очищаем базу перед тестом
        clear_all_arrays_for_test(self.test_db_path)
        
        start_time = time.time()
        successful = 0
        errors = []
        
        for i in range(count):
            # Генерируем случайный массив
            size = random.randint(*array_size_range)
            original = self.generate_random_array(size)
            sorted_arr, stats = tree_sort_with_stats(original)
            
            # Сохраняем в тестовую БД
            try:
                save_array(
                    user_id=1,  # тестовый пользователь
                    original_array=original,
                    sorted_array=sorted_arr,
                    comparisons=stats['comparisons'],
                    insertions=stats['insertions']
                )
                successful += 1
            except Exception as e:
                errors.append(f"Массив {i}: {e}")
        
        elapsed_time = time.time() - start_time
        final_count = get_arrays_count_for_test(self.test_db_path)
        
        result = {
            'test': 'add_arrays',
            'count': count,
            'successful': successful,
            'failed': count - successful,
            'time': elapsed_time,
            'time_per_array': elapsed_time / count if count > 0 else 0,
            'final_count': final_count,
            'errors': errors
        }
        
        print(f"Успешно добавлено: {successful}/{count}")
        print(f"Время выполнения: {elapsed_time:.4f} сек")
        print(f"Среднее время на массив: {result['time_per_array']:.6f} сек")
        print(f"Итоговое количество записей: {final_count}")
        
        if errors:
            print(f"  ❌ Ошибок: {len(errors)}")
        
        return result
    
    def test_load_and_sort(self, count: int) -> dict:
        """
        Тест выгрузки и сортировки массивов из базы данных
        """
        print(f"\n{'='*60}")
        print(f"ТЕСТ: Выгрузка и сортировка {count} массивов")
        print(f"{'='*60}")
        
        # Проверяем, что в базе достаточно записей
        db_count = get_arrays_count_for_test(self.test_db_path)
        
        if db_count < count:
            print(f"Внимание: в базе только {db_count} записей")
            count = db_count
        
        if count == 0:
            print(" Нет данных для тестирования")
            return {'test': 'load_and_sort', 'count': 0, 'successful': 0, 'time': 0}
        
        start_time = time.time()
        successful = 0
        total_comparisons = 0
        
        arrays = get_all_arrays_for_test(self.test_db_path)
        
        for i, arr in enumerate(arrays[:count]):
            original_text = arr['original_array']
            original = list(map(int, original_text.split()))
            
            # Сортируем заново
            sorted_arr, stats = tree_sort_with_stats(original)
            total_comparisons += stats['comparisons']
            
            # Проверяем корректность
            if is_sorted(sorted_arr):
                successful += 1
            else:
                print(f"  Ошибка: массив {i} не отсортирован корректно")
        
        elapsed_time = time.time() - start_time
        
        result = {
            'test': 'load_and_sort',
            'count': count,
            'successful': successful,
            'failed': count - successful,
            'time': elapsed_time,
            'time_per_array': elapsed_time / count if count > 0 else 0,
            'avg_comparisons': total_comparisons / count if count > 0 else 0
        }
        
        print(f"Успешно отсортировано: {successful}/{count}")
        print(f"Общее время: {elapsed_time:.4f} сек")
        print(f"Среднее время на массив: {result['time_per_array']:.6f} сек")
        print(f"Среднее количество сравнений: {result['avg_comparisons']:.0f}")
        
        return result
    
    def test_clear_database(self, count: int) -> dict:
        """
        Тест очистки базы данных
        """
        print(f"\n{'='*60}")
        print(f"ТЕСТ: Очистка базы данных ({count} записей)")
        print(f"{'='*60}")
        
        # Проверяем количество записей до очистки
        before_count = get_arrays_count_for_test(self.test_db_path)
        
        if before_count < count:
            print(f"В базе {before_count} записей (ожидалось {count})")
        
        start_time = time.time()
        deleted = clear_all_arrays_for_test(self.test_db_path)
        elapsed_time = time.time() - start_time
        
        after_count = get_arrays_count_for_test(self.test_db_path)
        
        result = {
            'test': 'clear_database',
            'expected_count': count,
            'before_count': before_count,
            'deleted': deleted,
            'after_count': after_count,
            'time': elapsed_time,
            'success': after_count == 0
        }
        
        print(f"Удалено записей: {deleted}")
        print(f"Время очистки: {elapsed_time:.4f} сек")
        print(f"База пуста: {after_count == 0}")
        
        return result
    
    def run_all_tests(self, counts=[100, 1000, 10000]):
        """
        Запуск всех тестов для разных объемов данных
        """
        print("\n" + "="*70)
        print("ЗАПУСК ИНТЕГРАЦИОННЫХ ТЕСТОВ ДЛЯ БАЗЫ ДАННЫХ")
        print("="*70)
        
        # Инициализируем тестовую БД
        init_db(self.test_db_path)
        
        all_results = {}
        
        for count in counts:
            print(f"\n{'█'*70}")
            print(f"Тестирование для {count} записей")
            print(f"{'█'*70}")
            
            # Тест 1: Добавление массивов
            result1 = self.test_add_arrays(count)
            all_results[f"add_{count}"] = result1
            
            # Тест 2: Выгрузка и сортировка
            result2 = self.test_load_and_sort(count)
            all_results[f"load_{count}"] = result2
            
            # Тест 3: Очистка базы
            result3 = self.test_clear_database(count)
            all_results[f"clear_{count}"] = result3
        
        # Вывод итоговой таблицы
        self.print_summary(all_results)
        
        return all_results
    
    def print_summary(self, results):
        """Выводит сводную таблицу результатов"""
        print("\n" + "="*70)
        print("СВОДНАЯ ТАБЛИЦА РЕЗУЛЬТАТОВ")
        print("="*70)
        
        print("\n{:<20} {:<15} {:<15} {:<15}".format("Тест", "Время (сек)", "Успешно", "Статус"))
        print("-"*70)
        
        for name, result in results.items():
            time_str = f"{result.get('time', 0):.4f}"
            success_str = f"{result.get('successful', 0)}/{result.get('count', 0)}"
            status = "✓" if result.get('successful', 0) == result.get('count', 0) else "✗"
            
            print("{:<20} {:<15} {:<15} {:<15}".format(name, time_str, success_str, status))
        
        print("\n" + "="*70)
        print("ВСЕ ТЕСТЫ ЗАВЕРШЕНЫ")
        print("="*70)


def run_tests():
    """Запуск всех тестов"""
    tester = TestDatabase()
    results = tester.run_all_tests(counts=[100, 1000, 10000])
    return results


if __name__ == "__main__":
    run_tests()
