import random
import os
from typing import List, Tuple


class InputHandler:
    @staticmethod
    def from_keyboard() -> Tuple[bool, List[int]]:
        print("Введите целые числа через пробел:")
        print("Например: 5 2 8 1 9 3 7 4 6")
        
        while True:
            try:
                input_str = input("> ").strip()
                if not input_str:
                    print("Ошибка: строка пуста. Попробуйте снова.")
                    continue
                
                arr = [int(x) for x in input_str.split()]
                print(f" Принято {len(arr)} чисел")
                return True, arr
            except ValueError:
                print("Ошибка: введите только целые числа через пробел.")
    
    @staticmethod
    def random_array() -> Tuple[bool, List[int]]:
        try:
            size = int(input("Введите размер массива: "))
            if size <= 0:
                print("Ошибка: размер должен быть положительным числом.")
                return False, []
            
            min_val = int(input("Введите минимальное значение: "))
            max_val = int(input("Введите максимальное значение: "))
            
            if min_val > max_val:
                print("Ошибка: минимальное значение не может быть больше максимального.")
                return False, []
            
            arr = [random.randint(min_val, max_val) for _ in range(size)]
            print(f" Сгенерирован массив из {size} элементов")
            return True, arr
        except ValueError:
            print("Ошибка: введите целые числа.")
            return False, []
    
    @staticmethod
    def from_file() -> Tuple[bool, List[int]]:
        """
        Загрузка массива из файла.
        Поддерживаются форматы: числа через пробел, через запятую, или каждое число с новой строки
        """
        print("\n--- Загрузка из файла ---")
        print("Поддерживаемые форматы:")
        print("  1. Числа через пробел: 5 2 8 1 9")
        print("  2. Числа через запятую: 5,2,8,1,9")
        print("  3. Каждое число с новой строки:")
        print("     5")
        print("     2")
        print("     8")
        
        filename = input("\nВведите имя файла: ").strip()
        
        if not filename:
            print("Ошибка: имя файла не может быть пустым.")
            return False, []
        
        try:
            # Проверяем существование файла
            if not os.path.exists(filename):
                print(f"Ошибка: файл '{filename}' не найден.")
                print(f"Текущая папка: {os.getcwd()}")
                return False, []
            
            # Читаем файл
            with open(filename, 'r', encoding='utf-8') as file:
                content = file.read().strip()
                
            if not content:
                print("Ошибка: файл пуст.")
                return False, []
            
            # Пробуем разные способы парсинга
            arr = None
            
            # Способ 1: числа через пробел
            try:
                arr = [int(x) for x in content.split()]
                if arr:
                    print(f" Загружено {len(arr)} чисел (формат: через пробел)")
                    return True, arr
            except:
                pass
            
            # Способ 2: числа через запятую
            try:
                # Заменяем запятые на пробелы и удаляем лишние символы
                cleaned = content.replace(',', ' ').replace('\n', ' ').replace('\r', ' ')
                arr = [int(x) for x in cleaned.split() if x.strip()]
                if arr:
                    print(f" Загружено {len(arr)} чисел (формат: через запятую)")
                    return True, arr
            except:
                pass
            
            # Способ 3: числа построчно
            try:
                lines = content.split('\n')
                arr = []
                for line in lines:
                    line = line.strip()
                    if line and not line.startswith('#'):  # Пропускаем комментарии
                        # Если в строке несколько чисел через пробел
                        numbers = line.split()
                        if numbers:
                            arr.extend([int(x) for x in numbers])
                if arr:
                    print(f" Загружено {len(arr)} чисел (формат: построчно)")
                    return True, arr
            except:
                pass
            
            # Если ничего не сработало
            print("Ошибка: не удалось распознать формат данных в файле.")
            print("Используйте числа через пробел, запятую или каждое число с новой строки.")
            return False, []
            
        except FileNotFoundError:
            print(f"Ошибка: файл '{filename}' не найден.")
        except PermissionError:
            print(f"Ошибка: нет прав на чтение файла '{filename}'.")
        except UnicodeDecodeError:
            print(f"Ошибка: не удалось прочитать файл '{filename}'. Проверьте кодировку (должна быть UTF-8).")
        except Exception as e:
            print(f"Ошибка при чтении файла: {e}")
        
        return False, []
    
    @staticmethod
    def save_to_file(original: List[int], sorted_arr: List[int]) -> None:
        """
        Сохраняет исходный и отсортированный массивы в файл
        """
        print("\n--- Сохранение в файл ---")
        print("Совет: используйте имя с расширением .txt (например: result.txt)")
        
        filename = input("Введите имя файла для сохранения: ").strip()
        
        if not filename:
            print("Ошибка: имя файла не может быть пустым.")
            return
        
        # Добавляем расширение .txt если его нет
        if '.' not in os.path.basename(filename):
            filename += '.txt'
            print(f" Добавлено расширение .txt: {filename}")
        
        try:
            # Проверяем, можно ли создать файл в указанном месте
            directory = os.path.dirname(filename)
            if directory and not os.path.exists(directory):
                try:
                    os.makedirs(directory)
                    print(f" Создана папка: {directory}")
                except:
                    print(f" Не удалось создать папку {directory}")
                    return
            
            with open(filename, 'w', encoding='utf-8') as file:
                file.write("=" * 50 + "\n")
                file.write("РЕЗУЛЬТАТ СОРТИРОВКИ МЕТОДОМ ДЕРЕВА\n")
                file.write("=" * 50 + "\n\n")
                
                file.write("ИСХОДНЫЙ МАССИВ:\n")
                file.write("-" * 30 + "\n")
                file.write(f"Количество элементов: {len(original)}\n")
                file.write(" ".join(map(str, original)) + "\n\n")
                
                file.write("ОТСОРТИРОВАННЫЙ МАССИВ:\n")
                file.write("-" * 30 + "\n")
                file.write(f"Количество элементов: {len(sorted_arr)}\n")
                file.write(" ".join(map(str, sorted_arr)) + "\n\n")
                
                file.write("=" * 50 + "\n")
                from datetime import datetime
                file.write(f"Дата сохранения: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n")
            
            print(f" Массивы успешно сохранены в файл: {filename}")
            print(f" Полный путь: {os.path.abspath(filename)}")
            
        except PermissionError:
            print(f" Ошибка доступа: нет прав на запись в {filename}")
            print(" Попробуйте сохранить в другую папку (например: result.txt)")
        except Exception as e:
            print(f" Ошибка при сохранении: {e}")
