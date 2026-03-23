"""
Модуль для авторизации и регистрации пользователей
"""

import sqlite3
import hashlib
from database import get_db, init_db


def hash_password(password):
    """
    Хеширование пароля с использованием SHA-256
    """
    salt = "tree_sort_lab3_salt"
    return hashlib.sha256((password + salt).encode()).hexdigest()


def register_user(username, password):
    """
    Регистрация нового пользователя
    """
    if not username or not password:
        return False, "Логин и пароль не могут быть пустыми"
    
    if len(username) < 3:
        return False, "Логин должен содержать минимум 3 символа"
    
    if len(password) < 4:
        return False, "Пароль должен содержать минимум 4 символа"
    
    with get_db() as conn:
        cursor = conn.cursor()
        try:
            cursor.execute('''
                INSERT INTO users (username, password)
                VALUES (?, ?)
            ''', (username, hash_password(password)))
            conn.commit()
            return True, f"Пользователь {username} успешно зарегистрирован"
        except sqlite3.IntegrityError:
            return False, "Пользователь с таким логином уже существует"


def login_user(username, password):
    """
    Авторизация пользователя
    """
    if not username or not password:
        return False, "Введите логин и пароль"
    
    with get_db() as conn:
        cursor = conn.cursor()
        cursor.execute('''
            SELECT id FROM users 
            WHERE username = ? AND password = ?
        ''', (username, hash_password(password)))
        user = cursor.fetchone()
        
        if user:
            return True, user['id']
        else:
            return False, "Неверный логин или пароль"


def get_user_by_id(user_id):
    """
    Получить информацию о пользователе по ID
    """
    with get_db() as conn:
        cursor = conn.cursor()
        cursor.execute('SELECT id, username, created_at FROM users WHERE id = ?', (user_id,))
        return cursor.fetchone()


def user_exists(username):
    """
    Проверяет, существует ли пользователь
    """
    with get_db() as conn:
        cursor = conn.cursor()
        cursor.execute('SELECT id FROM users WHERE username = ?', (username,))
        return cursor.fetchone() is not None


# Инициализируем БД при импорте
init_db()
