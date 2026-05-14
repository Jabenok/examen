# Задание 1 (ПМ.01). Разработайте иерархию классов: абстрактный
# класс Employee (поля: имя, ставка) и классы-наследники HourlyEmployee (почасовая оплата) и SalaryEmployee (оклад).
# Реализуйте метод calculate_pay() для каждого.

# Задание 2 (ПМ.02). Создайте модуль ReportGenerator, который формирует
# текстовый отчёт по всем сотрудникам (имя, начисленная сумма).
# Интегрируйте его с системой расчёта зарплаты.

# Задание 3 (Отладка). Реализуйте обработку исключений (отрицательная
# ставка, некорректные часы). Продемонстрируйте работу с блоком try-except. 


from abc import ABC, abstractmethod

class Employee(ABC):
    def __init__(self, name, rate):
        self.name = name    
        if rate <=0:
            raise ValueError("Ставка должна быть положительной")

        self.rate=rate   
        # rate - почасовая ставка, оклад работника за день (12ч) - rate *12 



    @abstractmethod
    def calculate_pay(self):
        pass


class HourlyEmployee(Employee):
    def __init__(self, name, rate, hours):
        super().__init__(name, rate)
        if hours <0:
            raise ValueError("Кол-во часов должно быть больше 1")
        self.hours = hours

    def calculate_pay(self):
        return self.rate * self.hours
    
class SalaryEmployee(Employee):
    def __init__(self, name, rate, days):
        super().__init__(name, rate)
        self.days=days

    def calculate_pay(self):
        return self.rate * 12 * self.days 


class ReportGenerator:
    @staticmethod
    def generate_report(employees):
        for emp in employees:
            print(f"name: {emp.name}, pay: {emp.calculate_pay()}")
        


try:  
    employer1=HourlyEmployee("Иван", 100, 40)
    employer2=SalaryEmployee("Петр", 200, 20)
except ValueError as e:
    print(f"Ошибка: {e}")

ReportGenerator.generate_report([employer1, employer2])