# Задание 1 (ПМ.01). Разработайте
# класс User (поля: id, login, password_hash, role) и класс AuthService с
# методами register() и login(). Реализуйте проверку уникальности логина и
# хеширование пароля.

# Задание 2 (ПМ.02). Создайте модуль FileStorage для сохранения коллекции
# пользователей в JSON-файл и загрузки из него. Интегрируйте его
# с AuthService так, чтобы данные автоматически сохранялись при
# регистрации.

# Задание 3 (Отладка). Реализуйте класс Logger с методами info() и error().
# Добавьте вызовы логирования в методы register() и login(). Сымитируйте
# ошибку ввода неверного пароля и продемонстрируйте запись ошибки в логфайл

import json
import os
import hashlib
from datetime import datetime

def hash_password(password):
    return hashlib.sha256(password.encode()).hexdigest()


class User:
    def __init__(self, user_id, login, password_hash, role):
        self.id = user_id
        self.login = login
        self.password_hash = password_hash
        self.role = role

    def to_dict(self):
        return self.__dict__

class FileStorage:
    def __init__(self, filename='users.json'):
        self.filename = filename

    def load_from_file(self):
        if not os.path.exists(self.filename):
            return []
        try:
            with open(self.filename, 'r', encoding='utf-8') as file:
                return json.load(file)
        except (json.JSONDecodeError, IOError):
            return []

    @staticmethod
    def save_users(users_list, filename='users.json'):
        with open(filename, 'w', encoding='utf-8') as file:
            json.dump(users_list, file, indent=4, ensure_ascii=False)

class AuthService:
    def __init__(self):
        # 1. Создаем объект стораджа
        self.storage = FileStorage()
        # 2. Загружаем актуальные данные из файла СРАЗУ при старте
        self.users_list = self.storage.load_from_file()

    def register(self, login, password_hash, role):
        # 3. Проверка (теперь список self.users_list содержит данные из файла)
        for user in self.users_list:
            if user['login'] == login:
                Logger.error(f"Попытка зарегистрировать уже существующий логин: {login}")
                return f"Ошибка: пользователь {login} уже есть!"

        hashed = hash_password(password_hash)

        # 4. Создание нового
        new_id = len(self.users_list) + 1
        new_user = User(new_id, login, hashed, role)
        
        # 5. Добавляем в локальный список
        self.users_list.append(new_user.to_dict())
        
        # 6. Сохраняем ВЕСЬ обновленный список в файл
        FileStorage.save_users(self.users_list)
        Logger.info(f"Пользователь {login} успешно зарегистрирован.")
        return f"Пользователь {login} успешно зарегистрирован!"
    

    def login(self, login, password_hash):
        hashed = hash_password(password_hash)
        for user in self.users_list:
            if user['login']==login and user['password_hash'] == hashed:
                Logger.info(f"Пользователь {login} успешно вошел!")
                return f"Пользователь {login} успешно вошел!"
        Logger.error(f"Попытка входа с неверным паролем для пользователя: {login}")
        return f"Ошибка: пользователь {login} не найден!"


class Logger:
    FILE_NAME='app.log'

    @staticmethod
    def _write(level, message):
        timestamp = datetime.now().strftime('%d-%m-%Y %H:%M:%S')
        log_entry = f"{timestamp} [{level}] {message}\n"
        with open(Logger.FILE_NAME, 'a', encoding='utf-8') as log_file:
            log_file.write(log_entry)

    @staticmethod
    def info(message):
        print(f"[INFO] {message}")
        Logger._write("INFO", message)

    @staticmethod
    def error(message):
        print(f"[ERROR] {message}")
        Logger._write("ERROR", message)


def main():
    # Создаем ОДИН экземпляр сервиса на всё время работы
    auth = AuthService()

    while True:
        print("\n" + "="*20)
        print("ГЛАВНОЕ МЕНЮ")
        print("="*20)
        print("1. Регистрация")
        print("2. Вход в систему")
        print("3. Выход")
        
        choice = input("\nВыберите действие (1-3): ")

        if choice == '1':
            print("\n--- Регистрация ---")
            login = input("Введите логин: ")
            password = input("Введите пароль: ")
            role = input("Введите роль (admin/user): ")
            
            # Вызываем метод регистрации
            result = auth.register(login, password, role)
            print(f"\nРезультат: {result}")

        elif choice == '2':
            print("\n--- Вход ---")
            login = input("Логин: ")
            password = input("Пароль: ")
            
            # Вызываем метод логина
            result = auth.login(login, password)
            print(f"\nРезультат: {result}")

        elif choice == '3':
            print("Завершение работы. До свидания!")
            break

        else:
            print("Ошибка: неверный ввод. Попробуйте еще раз.")

if __name__ == "__main__":
    main()
