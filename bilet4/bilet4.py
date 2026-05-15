# Задание 1 (ПМ.01). Разработайте класс Logger с поддержкой трёх уровней
# логирования (INFO, WARNING, ERROR). Метод log(level, message) должен
# добавлять запись с временной меткой.

# Задание 2 (ПМ.02). Реализуйте модуль LogFileManager, который
# автоматически создаёт новый файл лога каждый день и очищает логи старше
# 7 дней. Интегрируйте с классом Logger.

# Задание 3 (Отладка). Напишите метод, который генерирует несколько
# исключений (деление на ноль, ошибка индекса). Покажите, как логгер
# фиксирует каждую ошибку с указанием типа исключения.
from datetime import datetime, timedelta
import os


class Logger:
    @staticmethod
    def Log(level, message, file):
        timestamp=datetime.now().strftime("%d-%m-%Y %H:%M:%S")
        log_message=f"{timestamp} - {level} - {message}"

        with open(file, "a") as log_file:
            log_file.write(log_message + "\n")

class LogFileManager:

    @staticmethod
    def create_log_file():
        today = datetime.now().strftime("%d-%m-%Y")
        log_file = f"log_{today}.txt"
        return log_file
    
    @staticmethod
    def clean_old_logs():
        today = datetime.now()
        for i in range(7, 30):
            old_date = (today - timedelta(days=i)).strftime("%d-%m-%Y")
            old_log_file = f"log_{old_date}.txt"
            try:
                os.remove(old_log_file)
            except FileNotFoundError:
                pass

def generate_exceptions():
    log_file = LogFileManager.create_log_file()
    try:
        result = 10 / 0
    except ZeroDivisionError as e:
        Logger.Log("ERROR", f"ZeroDivisionError: {e}", log_file)

    try:
        lst = [1, 2, 3]
        item = lst[5]
    except IndexError as e:
        Logger.Log("ERROR", f"IndexError: {e}", log_file)

if __name__ == "__main__":
    log_file = LogFileManager.create_log_file()
    Logger.Log("INFO", "Logger initialized", log_file)
    LogFileManager.clean_old_logs()
    generate_exceptions()