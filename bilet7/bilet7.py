from abc import ABC, abstractmethod


# --- Интерфейс для паттерна Декоратор ---
class ICart(ABC):

    @abstractmethod
    def get_total(self) -> float:
        pass

    @abstractmethod
    def get_item_count(self) -> int:
        pass


# --- Задание 1: Основные классы ---
class Product:

    def __init__(self, product_id: int, name: str, price: float):
        # Задание 3: Валидация цены при создании товара
        if price < 0:
            raise ValueError("Цена товара не может быть отрицательной.")

        self.id = product_id
        self.name = name
        self.price = price


class Cart(ICart):

    def __init__(self):
        # Храним товары в списке
        self._items = []

    def add_item(self, product: Product):
        self._items.append(product)

    def remove_item(self, product_id: int):
        # Удаляем первое совпадение по id товара
        for item in self._items:
            if item.id == product_id:
                self._items.remove(item)
                break

    def get_total(self) -> float:
        """Возвращает полную стоимость товаров в корзине."""
        return sum(item.price for item in self._items)

    def get_item_count(self) -> int:
        """Возвращает общее количество товаров в корзине."""
        return len(self._items)


# --- Задание 2: Модуль DiscountService (Декоратор) ---
class DiscountService(ICart):
    """Декоратор, который динамически добавляет логику расчета скидки к корзине."""

    def __init__(self, cart: ICart):
        self._cart = cart

    def get_item_count(self) -> int:
        # Делегируем вызов обернутому объекту корзины
        return self._cart.get_item_count()

    def get_total(self) -> float:
        """Вычисляет стоимость с учетом скидки (10% при сумме > 1000)."""
        base_total = self._cart.get_total()

        if base_total > 1000:
            return base_total * 0.90  # Применяем скидку 10%
        return base_total