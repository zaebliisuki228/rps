"""
Модуль для работы с базой данных SQLite
"""

import sqlite3
import os
from contextlib import contextmanager
from typing import List, Optional

# Путь к базе данных
DB_DIR = os.path.join(os.path.dirname(__file__), 'data')
DB_PATH = os.path.join(DB_DIR, 'database.db')
TEST_DB_PATH = os.path.join(DB_DIR, 'test_database.db')


def ensure_db_dir():
    """Создает папку для базы данных, если её нет"""
    if not os.path.exists(DB_DIR):
        os.makedirs(DB_DIR)


@contextmanager
def get_db(db_path=DB_PATH):
    """
    Контекстный менеджер для работы с БД
    """
    ensure_db_dir()
    conn = sqlite3.connect(db_path)
    conn.row_factory = sqlite3.Row  # доступ по именам колонок
    try:
        yield conn
    finally:
        conn.close()


def init_db(db_path=DB_PATH):
    """
    Инициализация базы данных: создание таблиц и индексов
    """
    with get_db(db_path) as conn:
        cursor = conn.cursor()
        
        # Таблица пользователей
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS users (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                username TEXT UNIQUE NOT NULL,
                password TEXT NOT NULL,
                created_at DATETIME DEFAULT CURRENT_TIMESTAMP
            )
        ''')
        
        # Таблица массивов
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS arrays (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                user_id INTEGER NOT NULL,
                original_array TEXT NOT NULL,
                sorted_array TEXT NOT NULL,
                size INTEGER NOT NULL,
                comparisons INTEGER DEFAULT 0,
                insertions INTEGER DEFAULT 0,
                created_at DATETIME DEFAULT CURRENT_TIMESTAMP,
                FOREIGN KEY (user_id) REFERENCES users(id) ON DELETE CASCADE
            )
        ''')
        
        # Индексы для ускорения запросов
        cursor.execute('CREATE INDEX IF NOT EXISTS idx_arrays_user_id ON arrays(user_id)')
        cursor.execute('CREATE INDEX IF NOT EXISTS idx_arrays_size ON arrays(size)')
        cursor.execute('CREATE INDEX IF NOT EXISTS idx_arrays_created ON arrays(created_at)')
        
        conn.commit()


def save_array(user_id: int, original_array: List[int], sorted_array: List[int], 
               comparisons: int = 0, insertions: int = 0) -> int:
    """
    Сохранить массив в базу данных
    """
    with get_db() as conn:
        cursor = conn.cursor()
        cursor.execute('''
            INSERT INTO arrays (user_id, original_array, sorted_array, size, comparisons, insertions)
            VALUES (?, ?, ?, ?, ?, ?)
        ''', (
            user_id,
            ' '.join(map(str, original_array)),
            ' '.join(map(str, sorted_array)),
            len(original_array),
            comparisons,
            insertions
        ))
        conn.commit()
        return cursor.lastrowid


def get_user_arrays(user_id: int, limit: int = 100) -> List[sqlite3.Row]:
    """
    Получить все массивы пользователя
    """
    with get_db() as conn:
        cursor = conn.cursor()
        cursor.execute('''
            SELECT * FROM arrays 
            WHERE user_id = ? 
            ORDER BY created_at DESC
            LIMIT ?
        ''', (user_id, limit))
        return cursor.fetchall()


def get_array_by_id(array_id: int, user_id: int) -> Optional[sqlite3.Row]:
    """
    Получить массив по ID
    """
    with get_db() as conn:
        cursor = conn.cursor()
        cursor.execute('''
            SELECT * FROM arrays 
            WHERE id = ? AND user_id = ?
        ''', (array_id, user_id))
        return cursor.fetchone()


def delete_array(array_id: int, user_id: int) -> bool:
    """
    Удалить массив по ID 
    """
    with get_db() as conn:
        cursor = conn.cursor()
        cursor.execute('DELETE FROM arrays WHERE id = ? AND user_id = ?', (array_id, user_id))
        conn.commit()
        return cursor.rowcount > 0


def get_all_arrays_for_test(db_path=TEST_DB_PATH) -> List[sqlite3.Row]:
    """
    Получить все массивы 
    """
    with get_db(db_path) as conn:
        cursor = conn.cursor()
        cursor.execute('SELECT * FROM arrays ORDER BY id')
        return cursor.fetchall()


def clear_all_arrays_for_test(db_path=TEST_DB_PATH) -> int:
    """
    Очистить все массивы (для тестов)
    """
    with get_db(db_path) as conn:
        cursor = conn.cursor()
        cursor.execute('DELETE FROM arrays')
        conn.commit()
        return cursor.rowcount


def get_arrays_count_for_test(db_path=TEST_DB_PATH) -> int:
    """
    Получить количество массивов (для тестов)
    """
    with get_db(db_path) as conn:
        cursor = conn.cursor()
        cursor.execute('SELECT COUNT(*) as count FROM arrays')
        return cursor.fetchone()['count']
