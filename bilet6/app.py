# Задание 1 (ПМ.01). Разработайте класс LogParser, который читает файл лога
# сервера. Метод parse_ip() должен извлекать все IP-адреса,
# метод count_requests() — подсчитывать количество запросов.

# Задание 2 (ПМ.02). Реализуйте модуль ReportBuilder, который формирует
# отчёт о топ-5 самых частых IP-адресов в формате JSON. Интегрируйте его
# с LogParser.

# Задание 3 (Отладка). Напишите тесты для проверки корректности
# извлечения IP-адресов из разных форматов строк лога (минимум 3 формата)

import json
import re
from collections import Counter


class LogParser:
    """Класс для чтения и анализа серверных логов."""

    def __init__(self, log_file_path: str = None):
        self.log_file_path = log_file_path
        # Регулярное выражение для поиска IPv4 адресов
        self.ip_pattern = re.compile(r"\b(?:\d{1,3}\.){3}\d{1,3}\b")

    def parse_ips_from_string(self, log_line: str) -> list:
        """Вспомогательный метод для извлечения IP из одной строки лога."""
        return self.ip_pattern.findall(log_line)

    def parse_ip(self) -> list:
        """Читает файл и извлекает все IP-адреса."""
        if not self.log_file_path:
            raise ValueError("Путь к файлу лога не задан.")

        ip_addresses = []
        try:
            with open(self.log_file_path, "r", encoding="utf-8") as file:
                for line in file:
                    ip_addresses.extend(self.parse_ips_from_string(line))
        except FileNotFoundError:
            print(f"Ошибка: Файл {self.log_file_path} не найден.")
        return ip_addresses

    def count_requests(self) -> int:
        """Подсчитывает общее количество запросов (строк) в логе."""
        if not self.log_file_path:
            raise ValueError("Путь к файлу лога не задан.")

        try:
            with open(self.log_file_path, "r", encoding="utf-8") as file:
                return sum(1 for _ in file)
        except FileNotFoundError:
            print(f"Ошибка: Файл {self.log_file_path} не найден.")
            return 0


class ReportBuilder:
    """Класс для формирования отчетов на основе данных из LogParser."""

    def __init__(self, parser: LogParser):
        self.parser = parser

    def generate_top_ips_json(self, top_n: int = 5) -> str:
        """Формирует JSON-отчет о топ-N самых частых IP-адресов."""
        ips = self.parser.parse_ip()
        total_requests = self.parser.count_requests()

        # Подсчет частоты IP-адресов
        ip_counts = Counter(ips)
        top_ips = ip_counts.most_common(top_n)

        # Формирование структуры отчета
        report_data = {
            "metadata": {
                "total_requests": total_requests,
                "unique_ips_found": len(ip_counts),
            },
            "top_ips": [
                {"ip": ip, "count": count} for ip, count in top_ips
            ],
        }

        # Возвращаем JSON-строку с красивыми отступами
        return json.dumps(report_data, indent=4)