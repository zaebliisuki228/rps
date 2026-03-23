"""
Модуль графического интерфейса для сортировки деревом
"""

import tkinter as tk
from tkinter import ttk, messagebox, scrolledtext
import random
from tree_sort import tree_sort_with_stats, is_sorted
from database import save_array, get_user_arrays, delete_array
from auth import register_user, login_user


class TreeSortApp:
    """Главный класс приложения"""
    
    def __init__(self, root):
        self.root = root
        self.root.title("Tree Sort - Сортировка деревом")
        self.root.geometry("950x700")
        self.root.minsize(850, 650)
        
        self.current_user_id = None
        self.current_username = None
        self.current_original = []
        self.current_sorted = []
        
        # Создаем экран входа
        self.create_login_frame()
    
    def clear_window(self):
        """Очищает окно от всех виджетов"""
        for widget in self.root.winfo_children():
            widget.destroy()
    
    def create_login_frame(self):
        """Создает экран входа/регистрации"""
        self.clear_window()
        
        # Центрируем фрейм
        main_frame = ttk.Frame(self.root)
        main_frame.place(relx=0.5, rely=0.5, anchor='center')
        
        # Заголовок
        ttk.Label(main_frame, text="Сортировка деревом (Tree Sort)", 
                  font=("Arial", 18, "bold")).pack(pady=20)
        ttk.Label(main_frame, text="Лабораторная работа №3", 
                  font=("Arial", 10)).pack(pady=(0, 20))
        
        # Рамка для формы входа
        login_frame = ttk.LabelFrame(main_frame, text="Вход в систему", padding=15)
        login_frame.pack(pady=10)
        
        ttk.Label(login_frame, text="Логин:").grid(row=0, column=0, sticky='w', pady=5)
        self.login_entry = ttk.Entry(login_frame, width=25)
        self.login_entry.grid(row=0, column=1, padx=10, pady=5)
        
        ttk.Label(login_frame, text="Пароль:").grid(row=1, column=0, sticky='w', pady=5)
        self.password_entry = ttk.Entry(login_frame, show="*", width=25)
        self.password_entry.grid(row=1, column=1, padx=10, pady=5)
        
        # Кнопки
        btn_frame = ttk.Frame(login_frame)
        btn_frame.grid(row=2, column=0, columnspan=2, pady=15)
        
        ttk.Button(btn_frame, text="Войти", command=self.login).pack(side=tk.LEFT, padx=5)
        ttk.Button(btn_frame, text="Регистрация", command=self.register).pack(side=tk.LEFT, padx=5)
        
        # Справка
        ttk.Button(main_frame, text="Справка", command=self.show_help).pack(pady=10)
        
        # Привязываем Enter для входа
        self.login_entry.bind('<Return>', lambda e: self.login())
        self.password_entry.bind('<Return>', lambda e: self.login())
    
    def create_main_frame(self):
        """Создает главный экран приложения"""
        self.clear_window()
        
        # ========== Верхняя панель ==========
        top_frame = ttk.Frame(self.root, padding="10")
        top_frame.pack(fill=tk.X)
        
        ttk.Label(top_frame, text=f"Пользователь: {self.current_username}", 
                  font=("Arial", 10, "bold")).pack(side=tk.LEFT)
        
        ttk.Button(top_frame, text="Выйти", command=self.logout).pack(side=tk.RIGHT)
        
        # ========== Основная панель ==========
        main_panel = ttk.PanedWindow(self.root, orient=tk.HORIZONTAL)
        main_panel.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)
        
        # ========== Левая панель - работа с массивом ==========
        left_frame = ttk.LabelFrame(main_panel, text="Работа с массивом", padding=10)
        main_panel.add(left_frame, weight=1)
        
        # ========== Настройки генерации массива ==========
        gen_frame = ttk.LabelFrame(left_frame, text="Настройки генерации", padding=5)
        gen_frame.pack(fill=tk.X, pady=(0, 10))
        
        # Первая строка: размер массива
        size_row = ttk.Frame(gen_frame)
        size_row.pack(fill=tk.X, pady=2)
        
        ttk.Label(size_row, text="Размер массива:").pack(side=tk.LEFT, padx=5)
        
        # Выбор размера массива (от 3 до 1000)
        self.array_size_var = tk.IntVar(value=10)
        size_spinbox = ttk.Spinbox(size_row, from_=3, to=1000, width=6, 
                                    textvariable=self.array_size_var,
                                    increment=1)
        size_spinbox.pack(side=tk.LEFT, padx=5)
        
        ttk.Label(size_row, text="(от 3 до 1000)").pack(side=tk.LEFT, padx=5)
        
        # Кнопки быстрого выбора размера
        size_preset_frame = ttk.Frame(gen_frame)
        size_preset_frame.pack(fill=tk.X, pady=2)
        
        ttk.Label(size_preset_frame, text="Быстрый выбор:").pack(side=tk.LEFT, padx=5)
        
        ttk.Button(size_preset_frame, text="10", width=3,
                   command=lambda: self.set_array_size(10)).pack(side=tk.LEFT, padx=2)
        ttk.Button(size_preset_frame, text="50", width=3,
                   command=lambda: self.set_array_size(50)).pack(side=tk.LEFT, padx=2)
        ttk.Button(size_preset_frame, text="100", width=3,
                   command=lambda: self.set_array_size(100)).pack(side=tk.LEFT, padx=2)
        ttk.Button(size_preset_frame, text="500", width=3,
                   command=lambda: self.set_array_size(500)).pack(side=tk.LEFT, padx=2)
        ttk.Button(size_preset_frame, text="1000", width=4,
                   command=lambda: self.set_array_size(1000)).pack(side=tk.LEFT, padx=2)
        
        # Вторая строка: диапазон значений
        range_row = ttk.Frame(gen_frame)
        range_row.pack(fill=tk.X, pady=2)
        
        ttk.Label(range_row, text="Диапазон значений:").pack(side=tk.LEFT, padx=5)
        
        # Минимальное значение
        self.min_val_var = tk.IntVar(value=-100)
        min_spinbox = ttk.Spinbox(range_row, from_=-10000, to=10000, width=6,
                                   textvariable=self.min_val_var,
                                   increment=10)
        min_spinbox.pack(side=tk.LEFT, padx=2)
        
        ttk.Label(range_row, text="до").pack(side=tk.LEFT, padx=2)
        
        # Максимальное значение
        self.max_val_var = tk.IntVar(value=100)
        max_spinbox = ttk.Spinbox(range_row, from_=-10000, to=10000, width=6,
                                   textvariable=self.max_val_var,
                                   increment=10)
        max_spinbox.pack(side=tk.LEFT, padx=2)
        
        # Кнопки быстрого выбора диапазона
        range_preset_frame = ttk.Frame(gen_frame)
        range_preset_frame.pack(fill=tk.X, pady=2)
        
        ttk.Label(range_preset_frame, text="Диапазоны:").pack(side=tk.LEFT, padx=5)
        
        ttk.Button(range_preset_frame, text="-100..100", width=9,
                   command=lambda: self.set_range(-100, 100)).pack(side=tk.LEFT, padx=2)
        ttk.Button(range_preset_frame, text="-1000..1000", width=10,
                   command=lambda: self.set_range(-1000, 1000)).pack(side=tk.LEFT, padx=2)
        ttk.Button(range_preset_frame, text="0..100", width=7,
                   command=lambda: self.set_range(0, 100)).pack(side=tk.LEFT, padx=2)
        ttk.Button(range_preset_frame, text="-50..50", width=7,
                   command=lambda: self.set_range(-50, 50)).pack(side=tk.LEFT, padx=2)
        
        # ========== ПОЛЕ ДЛЯ РУЧНОГО ВВОДА ==========
        input_frame = ttk.LabelFrame(left_frame, text="Ручной ввод массива", padding=5)
        input_frame.pack(fill=tk.X, pady=(0, 10))
        
        ttk.Label(input_frame, text="Введите числа через пробел:").pack(anchor=tk.W)
        self.input_entry = ttk.Entry(input_frame, width=60)
        self.input_entry.pack(fill=tk.X, pady=5)
        
        # Кнопка для загрузки введенного массива
        ttk.Button(input_frame, text="Загрузить массив", 
                   command=self.load_manual_array).pack(pady=2)
        
        # ========== ОТОБРАЖЕНИЕ МАССИВОВ ==========
        display_frame = ttk.LabelFrame(left_frame, text="Массивы", padding=5)
        display_frame.pack(fill=tk.BOTH, expand=True)
        
        # Исходный массив
        ttk.Label(display_frame, text="Исходный массив:", font=("Arial", 9, "bold")).pack(anchor=tk.W, pady=(5, 0))
        self.original_text = scrolledtext.ScrolledText(display_frame, height=6, font=("Courier", 9), wrap=tk.WORD)
        self.original_text.pack(fill=tk.BOTH, expand=True, pady=5)
        
        # Отсортированный массив
        ttk.Label(display_frame, text="Отсортированный массив:", font=("Arial", 9, "bold")).pack(anchor=tk.W)
        self.sorted_text = scrolledtext.ScrolledText(display_frame, height=6, font=("Courier", 9), wrap=tk.WORD)
        self.sorted_text.pack(fill=tk.BOTH, expand=True, pady=5)
        
        # Кнопки действий
        btn_frame = ttk.Frame(left_frame)
        btn_frame.pack(fill=tk.X, pady=10)
        
        ttk.Button(btn_frame, text="Случайный массив", 
                   command=self.generate_random).pack(side=tk.LEFT, padx=2, expand=True, fill=tk.X)
        ttk.Button(btn_frame, text="Сортировать", 
                   command=self.sort_array).pack(side=tk.LEFT, padx=2, expand=True, fill=tk.X)
        ttk.Button(btn_frame, text="Сохранить", 
                   command=self.save_array).pack(side=tk.LEFT, padx=2, expand=True, fill=tk.X)
        ttk.Button(btn_frame, text="Очистить", 
                   command=self.clear_arrays).pack(side=tk.LEFT, padx=2, expand=True, fill=tk.X)
        
        # Статистика
        stats_frame = ttk.LabelFrame(left_frame, text="Статистика сортировки", padding=5)
        stats_frame.pack(fill=tk.X, pady=10)
        
        self.stats_label = ttk.Label(stats_frame, text="Не отсортировано", foreground="gray")
        self.stats_label.pack(anchor=tk.W)
        
        # ========== Правая панель - сохраненные массивы ==========
        right_frame = ttk.LabelFrame(main_panel, text="Сохраненные массивы", padding=10)
        main_panel.add(right_frame, weight=1)
        
        # Список с прокруткой
        list_frame = ttk.Frame(right_frame)
        list_frame.pack(fill=tk.BOTH, expand=True)
        
        scrollbar = ttk.Scrollbar(list_frame)
        scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
        
        self.history_listbox = tk.Listbox(list_frame, yscrollcommand=scrollbar.set, 
                                           font=("Courier", 9), height=25)
        self.history_listbox.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
        scrollbar.config(command=self.history_listbox.yview)
        
        # Двойной клик для загрузки
        self.history_listbox.bind('<Double-Button-1>', lambda e: self.load_selected_array())
        
        # Кнопки управления историей
        hist_btn_frame = ttk.Frame(right_frame)
        hist_btn_frame.pack(fill=tk.X, pady=5)
        
        ttk.Button(hist_btn_frame, text="Обновить", 
                   command=self.load_history).pack(side=tk.LEFT, padx=2, expand=True, fill=tk.X)
        ttk.Button(hist_btn_frame, text="Загрузить", 
                   command=self.load_selected_array).pack(side=tk.LEFT, padx=2, expand=True, fill=tk.X)
        ttk.Button(hist_btn_frame, text="Удалить", 
                   command=self.delete_selected_array).pack(side=tk.LEFT, padx=2, expand=True, fill=tk.X)
        
        # Загружаем историю
        self.load_history()
    
    def load_manual_array(self):
        """Загружает вручную введенный массив в поле исходного массива"""
        text = self.input_entry.get().strip()
        if not text:
            messagebox.showwarning("Предупреждение", "Введите числа через пробел")
            return
        
        try:
            # Проверяем корректность ввода
            array = list(map(int, text.split()))
            
            # Проверяем размер
            if len(array) > 1000:
                if not messagebox.askyesno("Предупреждение", 
                                           f"Массив из {len(array)} элементов.\n"
                                           "Сортировка может занять время. Продолжить?"):
                    return
            
            # Загружаем массив
            self.current_original = array
            self.original_text.delete(1.0, tk.END)
            self.original_text.insert(1.0, ' '.join(map(str, array)))
            self.sorted_text.delete(1.0, tk.END)
            self.stats_label.config(text="Не отсортировано", foreground="gray")
            self.current_sorted = []
            
            messagebox.showinfo("Успех", f"Загружен массив из {len(array)} элементов")
            
        except ValueError:
            messagebox.showerror("Ошибка", "Некорректный ввод. Используйте целые числа через пробел")
    
    def set_array_size(self, size):
        """Устанавливает размер массива"""
        self.array_size_var.set(size)
    
    def set_range(self, min_val, max_val):
        """Устанавливает диапазон значений"""
        self.min_val_var.set(min_val)
        self.max_val_var.set(max_val)
    
    def show_help(self):
        """Показывает окно со справкой"""
        help_text = """
╔══════════════════════════════════════════════════════════════════════════════╗
║                         Tree Sort - Сортировка деревом                       ║
╚══════════════════════════════════════════════════════════════════════════════╝

【 РУЧНОЙ ВВОД МАССИВА 】
  1. В поле "Ручной ввод массива" введите числа через пробел
     Пример: 5 2 8 1 9 3 7 4 6
  2. Нажмите "Загрузить массив"
  3. Массив появится в поле "Исходный массив"
  4. Нажмите "Сортировать"

【 НАСТРОЙКИ ГЕНЕРАЦИИ 】
  • Размер массива: от 3 до 1000 элементов
  • Быстрый выбор: 10, 50, 100, 500, 1000
  • Диапазон значений: от -10000 до 10000

【 КАК РАБОТАТЬ 】
  1. Вход/Регистрация
     • Логин (минимум 3 символа) и пароль (минимум 4 символа)
     • Нажмите "Регистрация" для создания аккаунта
     • Нажмите "Войти" для входа

  2. Работа с массивом
     • Введите числа в поле ручного ввода и нажмите "Загрузить массив"
     • Или нажмите "Случайный массив" для генерации
     • Нажмите "Сортировать" для выполнения сортировки
     • Нажмите "Сохранить" для сохранения в базу данных
     • Нажмите "Очистить" для очистки полей

  3. История
     • Справа отображаются все сохраненные массивы
     • Двойной клик по элементу - загрузить массив
     • "Удалить" - удалить запись из базы

  4. Выход
     • Нажмите "Выйти" для возврата на экран входа

【 АЛГОРИТМ 】
  • Построение бинарного дерева поиска из элементов массива
  • Симметричный обход дерева для получения отсортированного списка

【 СТАТИСТИКА 】
  • Сравнения - сколько раз сравнивались числа
  • Вставки - сколько элементов добавлено в дерево (равно размеру массива)
  • Узлы - сколько узлов создано в дереве (равно размеру массива)

"""
        help_window = tk.Toplevel(self.root)
        help_window.title("Справка - Tree Sort")
        help_window.geometry("750x650")
        
        text_area = scrolledtext.ScrolledText(help_window, wrap=tk.WORD, font=("Courier", 9))
        text_area.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)
        text_area.insert(tk.END, help_text)
        text_area.config(state=tk.DISABLED)
        
        ttk.Button(help_window, text="Закрыть", command=help_window.destroy).pack(pady=5)
    
    def generate_random(self):
        """Генерирует случайный массив с заданными параметрами"""
        try:
            size = self.array_size_var.get()
            min_val = self.min_val_var.get()
            max_val = self.max_val_var.get()
            
            # Проверка размера
            if size < 3:
                size = 3
                self.array_size_var.set(3)
            if size > 1000:
                size = 1000
                self.array_size_var.set(1000)
            
            # Проверка диапазона
            if min_val > max_val:
                min_val, max_val = max_val, min_val
                self.min_val_var.set(min_val)
                self.max_val_var.set(max_val)
            
            # Генерация массива
            array = [random.randint(min_val, max_val) for _ in range(size)]
            self.current_original = array
            self.original_text.delete(1.0, tk.END)
            self.original_text.insert(1.0, ' '.join(map(str, array)))
            self.sorted_text.delete(1.0, tk.END)
            self.stats_label.config(text="Не отсортировано", foreground="gray")
            self.current_sorted = []
            
            # Очищаем поле ручного ввода
            self.input_entry.delete(0, tk.END)
            
            # Уведомление о размере для больших массивов
            if size > 500:
                messagebox.showinfo("Информация", 
                                    f"Сгенерирован массив из {size} элементов.\n"
                                    f"Для сортировки большого массива может потребоваться время.")
            
        except Exception as e:
            messagebox.showerror("Ошибка", str(e))
    
    def clear_arrays(self):
        """Очищает поля ввода"""
        self.input_entry.delete(0, tk.END)
        self.original_text.delete(1.0, tk.END)
        self.sorted_text.delete(1.0, tk.END)
        self.stats_label.config(text="Не отсортировано", foreground="gray")
        self.current_original = []
        self.current_sorted = []
    
    def sort_array(self):
        """Сортирует массив с выводом статистики"""
        try:
            # Получаем текст из поля исходного массива
            text = self.original_text.get(1.0, tk.END).strip()
            if not text:
                messagebox.showwarning("Предупреждение", 
                                      "Сначала загрузите или сгенерируйте массив!\n\n"
                                      "Варианты:\n"
                                      "1. Введите числа в поле 'Ручной ввод' и нажмите 'Загрузить массив'\n"
                                      "2. Нажмите 'Случайный массив' для генерации")
                return
            
            array = list(map(int, text.split()))
            self.current_original = array
            
            # Показываем, что сортировка началась
            self.root.config(cursor="watch")
            self.stats_label.config(text="Сортировка...", foreground="orange")
            self.root.update()
            
            # Сортируем со статистикой
            sorted_array, stats = tree_sort_with_stats(array)
            self.current_sorted = sorted_array
            
            # Показываем результат
            self.sorted_text.delete(1.0, tk.END)
            self.sorted_text.insert(1.0, ' '.join(map(str, sorted_array)))
            
            # Показываем статистику
            self.stats_label.config(
                text=f"Сравнений: {stats['comparisons']:,} | Вставок: {stats['insertions']:,} | Узлов: {stats['nodes']:,}",
                foreground="green"
            )
            
            if not is_sorted(sorted_array):
                messagebox.showwarning("Внимание", "Алгоритм вернул неотсортированный массив!")
            
            # Возвращаем курсор
            self.root.config(cursor="")
                
        except ValueError:
            self.root.config(cursor="")
            messagebox.showerror("Ошибка", "Некорректный ввод. Используйте целые числа через пробел")
        except Exception as e:
            self.root.config(cursor="")
            messagebox.showerror("Ошибка", str(e))
    
    def save_array(self):
        """Сохраняет массив в базу данных"""
        if not self.current_user_id:
            messagebox.showwarning("Предупреждение", "Сначала войдите в систему")
            return
        
        if not self.current_original or not self.current_sorted:
            messagebox.showwarning("Предупреждение", "Сначала отсортируйте массив")
            return
        
        try:
            # Получаем статистику (пересчитываем)
            _, stats = tree_sort_with_stats(self.current_original)
            
            save_array(
                self.current_user_id,
                self.current_original,
                self.current_sorted,
                stats['comparisons'],
                stats['insertions']
            )
            messagebox.showinfo("Успех", "Массив сохранен в базу данных")
            self.load_history()
            
        except Exception as e:
            messagebox.showerror("Ошибка", str(e))
    
    def load_history(self):
        """Загружает историю массивов пользователя"""
        if not self.current_user_id:
            return
        
        try:
            arrays = get_user_arrays(self.current_user_id)
            self.history_listbox.delete(0, tk.END)
            self.history_data = {}
            
            for arr in arrays:
                # Форматируем дату
                date = arr['created_at'][:16] if arr['created_at'] else "N/A"
                size = arr['size']
                comparisons = arr['comparisons'] or 0
                
                display = f"{date} | Размер: {size:4} | Сравнений: {comparisons:6,}"
                self.history_listbox.insert(tk.END, display)
                self.history_data[display] = arr['id']
                
            if arrays:
                self.history_listbox.selection_set(0)
                
        except Exception as e:
            print(f"Ошибка загрузки истории: {e}")
    
    def load_selected_array(self):
        """Загружает выбранный массив из истории"""
        selection = self.history_listbox.curselection()
        if not selection:
            messagebox.showwarning("Предупреждение", "Выберите массив из списка")
            return
        
        display = self.history_listbox.get(selection[0])
        array_id = self.history_data.get(display)
        
        if not array_id:
            return
        
        from database import get_array_by_id
        arr = get_array_by_id(array_id, self.current_user_id)
        
        if arr:
            self.original_text.delete(1.0, tk.END)
            self.original_text.insert(1.0, arr['original_array'])
            
            self.sorted_text.delete(1.0, tk.END)
            self.sorted_text.insert(1.0, arr['sorted_array'])
            
            self.current_original = list(map(int, arr['original_array'].split()))
            self.current_sorted = list(map(int, arr['sorted_array'].split()))
            
            self.stats_label.config(
                text=f"Сравнений: {arr['comparisons']:,} | Вставок: {arr['insertions']:,}",
                foreground="blue"
            )
            messagebox.showinfo("Загружено", "Массив загружен из истории")
    
    def delete_selected_array(self):
        """Удаляет выбранный массив из истории"""
        selection = self.history_listbox.curselection()
        if not selection:
            messagebox.showwarning("Предупреждение", "Выберите массив для удаления")
            return
        
        if not messagebox.askyesno("Подтверждение", "Удалить выбранный массив?"):
            return
        
        display = self.history_listbox.get(selection[0])
        array_id = self.history_data.get(display)
        
        if array_id and delete_array(array_id, self.current_user_id):
            messagebox.showinfo("Успех", "Массив удален")
            self.load_history()
        else:
            messagebox.showerror("Ошибка", "Не удалось удалить массив")
    
    def login(self):
        """Авторизация пользователя"""
        username = self.login_entry.get().strip()
        password = self.password_entry.get().strip()
        
        if not username or not password:
            messagebox.showwarning("Предупреждение", "Заполните все поля")
            return
        
        success, result = login_user(username, password)
        
        if success:
            self.current_user_id = result
            self.current_username = username
            self.create_main_frame()
        else:
            messagebox.showerror("Ошибка", result)
    
    def register(self):
        """Регистрация пользователя"""
        username = self.login_entry.get().strip()
        password = self.password_entry.get().strip()
        
        if not username or not password:
            messagebox.showwarning("Предупреждение", "Заполните все поля")
            return
        
        success, message = register_user(username, password)
        
        if success:
            messagebox.showinfo("Успех", message)
        else:
            messagebox.showerror("Ошибка", message)
    
    def logout(self):
        """Выход из системы"""
        self.current_user_id = None
        self.current_username = None
        self.current_original = []
        self.current_sorted = []
        self.create_login_frame()


def main():
    """Запуск приложения"""
    from database import init_db
    init_db()
    
    root = tk.Tk()
    app = TreeSortApp(root)
    root.mainloop()


if __name__ == "__main__":
    main()
