import csv
import os


class Statistics:
    @staticmethod
    def mean(numbers: list) -> float:
        if not numbers:
            return 0.0
        return sum(numbers) / len(numbers)

    @staticmethod
    def median(numbers: list) -> float:
        if not numbers:
            return 0.0
        
        sorted_nums = sorted(numbers)
        n = len(sorted_nums)
        mid = n // 2

        if n % 2 == 1:
            return float(sorted_nums[mid])
        else:
            return (sorted_nums[mid - 1] + sorted_nums[mid]) / 2.0

    @staticmethod
    def mode(numbers: list) -> list:
        if not numbers:
            return []
        
        frequencies = {}
        for num in numbers:
            frequencies[num] = frequencies.get(num, 0) + 1
            
        max_freq = max(frequencies.values())
        return [num for num, freq in frequencies.items() if freq == max_freq]


class DataAnalyzer:
    def __init__(self, statistics_engine: Statistics):
        self.stats = statistics_engine

    def analyze_csv_column(self, filename: str, column_name: str) -> dict:
        if not os.path.exists(filename):
            print(f"Ошибка: Файл '{filename}' не найден.")
            return {}

        numbers = []
        try:
            with open(filename, mode="r", encoding="utf-8") as f:
                reader = csv.DictReader(f)
                if column_name not in reader.fieldnames:
                    print(f"Ошибка: Столбец '{column_name}' отсутствует в файле.")
                    return {}
                
                for row in reader:
                    val = row.get(column_name)
                    if val is not None and val.strip() != "":
                        try:
                            numbers.append(float(val.strip()))
                        except ValueError:
                            continue
        except OSError as e:
            print(f"Ошибка чтения файла '{filename}': {e}")
            return {}

        if not numbers:
            print(f"Предупреждение: Нет числовых данных в столбце '{column_name}'.")
            return {}

        return {
            "mean": self.stats.mean(numbers),
            "median": self.stats.median(numbers),
            "mode": self.stats.mode(numbers)
        }


def test_median_calculation():
    print("--- Запуск тестов метода Statistics.median() ---")
    stats = Statistics()

    test_cases = [
        {"name": "Нечетное количество элементов", "data": [1, 3, 3, 6, 7, 8, 9], "expected": 6.0},
        {"name": "Четное количество элементов", "data": [1, 2, 3, 4, 5, 6, 8, 9], "expected": 4.5},
        {"name": "Неотсортированный список (четный)", "data": [9, 1, 3, 8, 2, 6, 4, 5], "expected": 4.5},
        {"name": "Пустой список", "data": [], "expected": 0.0},
        {"name": "Один элемент", "data": [42], "expected": 42.0}
    ]

    all_passed = True
    for case in test_cases:
        result = stats.median(case["data"])
        if result == case["expected"]:
            print(f"УСПЕШНО: [{case['name']}] Данные: {case['data']} -> Медиана: {result}")
        else:
            print(f"ОШИБКА: [{case['name']}] Ожидалось {case['expected']}, получено {result}")
            all_passed = False

    if all_passed:
        print("Все тесты для медианы успешно пройдены!\n")
    else:
        print("Обнаружены ошибки в тестах медианы.\n")


if __name__ == "__main__":
    test_median_calculation()

    print("--- Демонстрация работы анализатора данных ---")
    csv_filename = "analytics_data.csv"
    
    with open(csv_filename, mode="w", newline="", encoding="utf-8") as f:
        writer = csv.writer(f)
        writer.writerow(["item", "price", "quantity"])
        writer.writerow(["Laptop", "1200", "5"])
        writer.writerow(["Smartphone", "800", "12"])
        writer.writerow(["Tablet", "500", "8"])
        writer.writerow(["Monitor", "300", "8"])
        writer.writerow(["Mouse", "25", "25"])

    stats_engine = Statistics()
    analyzer = DataAnalyzer(stats_engine)

    print("Анализ цен товаров (столбец 'price'):")
    price_analysis = analyzer.analyze_csv_column(csv_filename, "price")
    print(price_analysis)

    print("\nАнализ количества товаров (столбец 'quantity'):")
    quantity_analysis = analyzer.analyze_csv_column(csv_filename, "quantity")
    print(quantity_analysis)

    if os.path.exists(csv_filename):
        os.remove(csv_filename)