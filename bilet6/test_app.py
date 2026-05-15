import unittest


class TestLogParser(unittest.TestCase):

    def setUp(self):
        # Инициализируем парсер без файла для тестирования строк напрямую
        self.parser = LogParser()

    def test_nginx_common_format(self):
        """Тест стандартного формата Nginx/Apache (IP в начале)"""
        line = '192.168.1.50 - - [15/May/2026:14:32:10 +0300] "GET /index.html HTTP/1.1" 200 4324'
        result = self.parser.parse_ips_from_string(line)
        self.assertEqual(result, ["192.168.1.50"])

    def test_json_log_format(self):
        """Тест лога в формате JSON"""
        line = '{"time": "2026-05-15T14:32:10Z", "remote_ip": "10.0.0.1", "status": 404, "request": "/api/v1/user"}'
        result = self.parser.parse_ips_from_string(line)
        self.assertEqual(result, ["10.0.0.1"])

    def test_w3c_and_custom_format(self):
        """Тест кастомного формата с портами и флагами (IP в середине)"""
        line = "Status: 500 | Client connected from: 172.16.254.1:8080 | Threads: 12"
        result = self.parser.parse_ips_from_string(line)
        self.assertEqual(result, ["172.16.254.1"])

    def test_no_ip_in_line(self):
        """Тест строки, в которой нет IP-адреса"""
        line = "Crashed successfully. Critical error in memory allocation."
        result = self.parser.parse_ips_from_string(line)
        self.assertEqual(result, [])


if __name__ == "__main__":
    # Запуск тестов
    unittest.main()