class Order:
    VALID_STATUSES = ["new", "paid", "shipped", "delivered"]

    def __init__(self, order_id: int, items: list):
        self.order_id = order_id
        self.items = items
        self._status = "new"

    @property
    def status(self) -> str:
        return self._status

    @status.setter
    def status(self, new_status: str):
        if new_status not in self.VALID_STATUSES:
            raise ValueError(f"Недопустимый статус заказа: '{new_status}'.")
        self._status = new_status


class NotificationService:
    @staticmethod
    def send_status_change_notification(order_id: int, old_status: str, new_status: str):
        print(f"[УВЕДОМЛЕНИЕ] Заказ #{order_id}: статус изменен с '{old_status}' на '{new_status}'")


class OrderManager:
    def __init__(self, notification_service: NotificationService):
        self.orders = {}
        self.notification_service = notification_service
        self._next_id = 1

    def create_order(self, items: list) -> Order:
        order = Order(self._next_id, items)
        self.orders[order.order_id] = order
        self._next_id += 1
        return order

    def update_status(self, order_id: int, new_status: str) -> bool:
        order = self.orders.get(order_id)
        if not order:
            print(f"[Ошибка] Заказ #{order_id} не найден.")
            return False

        old_status = order.status
        if old_status == new_status:
            return True

        try:
            order.status = new_status
            self.notification_service.send_status_change_notification(order_id, old_status, new_status)
            return True
        except ValueError as e:
            print(f"[Ошибка] Ошибка обновления статуса для заказа #{order_id}: {e}")
            return False

    def get_orders_by_status(self, status: str) -> list:
        return [order for order in self.orders.values() if order.status == status]


def test_invalid_status_transition():
    print("--- Запуск тестов валидации статусов ---")
    notifier = NotificationService()
    manager = OrderManager(notifier)
    order = manager.create_order(["Ноутбук", "Мышь"])

    print(f"Начальный статус заказа: '{order.status}'")

    success = manager.update_status(order.order_id, "paid")
    if success and order.status == "paid":
        print("Тест перевода в валидный статус: УСПЕШНО")
    else:
        print("Тест перевода в валидный статус: ОШИБКА")

    print("\nПопытка установки некорректного статуса ('invalid_status_name')...")
    success_invalid = manager.update_status(order.order_id, "invalid_status_name")

    if not success_invalid and order.status == "paid":
        print("Тест защиты от некорректного статуса: УСПЕШНО (изменение отклонено)")
    else:
        print("Тест защиты от некорректного статуса: ОШИБКА (статус изменился или метод вернул True)")


if __name__ == "__main__":
    test_invalid_status_transition()
    print("\n--- Демонстрация работы системы ---")

    notifier = NotificationService()
    manager = OrderManager(notifier)

    order1 = manager.create_order(["Смартфон"])
    order2 = manager.create_order(["Клавиатура", "Наушники"])

    manager.update_status(order1.order_id, "paid")
    manager.update_status(order1.order_id, "shipped")
    manager.update_status(order2.order_id, "paid")

    print(f"\nЗаказы со статусом 'paid': {[o.order_id for o in manager.get_orders_by_status('paid')]}")
    print(f"Заказы со статусом 'shipped': {[o.order_id for o in manager.get_orders_by_status('shipped')]}")