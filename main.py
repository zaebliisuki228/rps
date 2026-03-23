
import sys
import os
from typing import List
from tree_sort import TreeSorter
from input_handler import InputHandler
from test_tree_sort import run_tests


if sys.executable.endswith('pythonw.exe'):
    os.system('start cmd /k python main.py')
    sys.exit()


class Application:
    
    def __init__(self):
        self.input_handler = InputHandler()
        self.sorter = TreeSorter()
        self.running = True
    
    def clear_screen(self):
        os.system('cls' if os.name == 'nt' else 'clear')
    
    def show_header(self):
        print("=" * 45)
        print("ЛАБОРАТОРНАЯ РАБОТА №2")
        print("Сортировка деревом (Tree Sort)")
        print("Вариант 5, Смычкова М.Е., Группа 444")
        print("=" * 45)
    
    def show_menu(self):
        print("\n1. Ввод с клавиатуры")
        print("2. Случайная генерация")
        print("3. Загрузка из файла")
        print("4. Запустить тесты")
        print("5. Выход")
        print("-" * 45)
    
    def process_array(self, arr: List[int]) -> None:
        if not arr:
            print("\nОшибка: массив пуст.")
            return
        
        print(f"\nИсходный массив ({len(arr)} элементов):")
        print(" ".join(map(str, arr)))
        
        # Сортировка
        print("\nСортировка...")
        sorted_arr = self.sorter.sort(arr)
        print("Готово!")
        
        print(f"\nОтсортированный массив:")
        print(" ".join(map(str, sorted_arr)))
        
        # Предложение сохранить
        print("\n" + "-" * 45)
        save_choice = input("Сохранить оба массива в файл? (y/n): ").strip().lower()
        if save_choice in ['y', 'yes', 'да', 'д']:
            self.input_handler.save_to_file(arr, sorted_arr)
    
    def run(self):
        while self.running:
            self.clear_screen()
            self.show_header()
            self.show_menu()
            
            choice = input("Выберите: ").strip()
            
            if choice == '1':
                # Ввод с клавиатуры
                self.clear_screen()
                self.show_header()
                print("\n--- Ввод с клавиатуры ---")
                success, arr = self.input_handler.from_keyboard()
                if success:
                    self.process_array(arr)
                input("\nНажмите Enter чтобы продолжить...")
                
            elif choice == '2':
                # Случайная генерация
                self.clear_screen()
                self.show_header()
                print("\n--- Случайная генерация ---")
                success, arr = self.input_handler.random_array()
                if success:
                    self.process_array(arr)
                input("\nНажмите Enter чтобы продолжить...")
                
            elif choice == '3':
                # Загрузка из файла
                self.clear_screen()
                self.show_header()
                print("\n--- Загрузка из файла ---")
                success, arr = self.input_handler.from_file()
                if success:
                    self.process_array(arr)
                input("\nНажмите Enter чтобы продолжить...")
                
            elif choice == '4':
                # Запустить тесты
                self.clear_screen()
                self.show_header()
                print("\n--- ЗАПУСК ТЕСТОВ ---\n")
                run_tests()
                input("\nНажмите Enter чтобы продолжить...")
                
            elif choice == '5':
                # Выход
                print("\nДо свидания!")
                self.running = False
                
            else:
                print("\nОшибка: неверный выбор. Пожалуйста, выберите 1-5.")
                input("Нажмите Enter чтобы продолжить...")


def main():
    app = Application()
    try:
        app.run()
    except KeyboardInterrupt:
        print("\n\nПрограмма прервана пользователем. До свидания!")
    except Exception as e:
        print(f"\nКритическая ошибка: {e}")
        print("Пожалуйста, перезапустите программу.")
    
    return 0

if __name__ == "__main__":
    sys.exit(main())
