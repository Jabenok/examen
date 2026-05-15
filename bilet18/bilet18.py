import os


class Observer:
    def update(self, event_type: str, data: any):
        pass


class Subject:
    def __init__(self):
        self._observers = []

    def attach(self, observer: Observer):
        if observer not in self._observers:
            self._observers.append(observer)

    def detach(self, observer: Observer):
        if observer in self._observers:
            self._observers.remove(observer)

    def notify(self, event_type: str, data: any):
        for observer in self._observers:
            observer.update(event_type, data)


class EmailObserver(Observer):
    def __init__(self, email: str):
        self.email = email

    def update(self, event_type: str, data: any):
        print(f"[Email Bot] Отправлено письмо на {self.email} | Событие: {event_type} | Данные: {data}")


class LogObserver(Observer):
    def __init__(self, filename: str):
        self.filename = filename

    def update(self, event_type: str, data: any):
        try:
            with open(self.filename, mode="a", encoding="utf-8") as f:
                f.write(f"[LOG] Событие: {event_type} | Данные: {data}\n")
        except PermissionError:
            print(f"[Log Error] Нет прав на запись в файл лога '{self.filename}'.")
        except OSError as e:
            print(f"[Log Error] Ошибка ввода-вывода при записи лога: {e}")


if __name__ == "__main__":
    log_file = "notifications.log"
    if os.path.exists(log_file):
        os.remove(log_file)

    subject = Subject()

    email_sub = EmailObserver("manager@company.com")
    log_sub = LogObserver(log_file)

    subject.attach(email_sub)
    subject.attach(log_sub)

    print("--- Демонстрация (Событие: 'Новый заказ') ---")
    order_data = {"order_id": 404, "total": 15900, "items": ["SSD", "RAM"]}
    
    subject.notify("NEW_ORDER", order_data)

    print("\n--- Демонстрация (Отключение EmailObserver и новое событие) ---")
    subject.detach(email_sub)

    cancel_data = {"order_id": 404, "reason": "User cancellation"}
    subject.notify("CANCEL_ORDER", cancel_data)

    print("\n--- Содержимое созданного лог-файла ---")
    if os.path.exists(log_file):
        with open(log_file, "r", encoding="utf-8") as f:
            print(f.read().strip())
        os.remove(log_file)