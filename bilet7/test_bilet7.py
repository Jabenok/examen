import unittest


class TestECommerceSystem(unittest.TestCase):

    # --- Тесты Задания 3 (Валидация отрицательной цены) ---
    def test_product_creation_with_negative_price_raises_error(self):
        """Проверка, что создание товара с отрицательной ценой вызывает ошибку ValueError."""
        with self.assertRaises(ValueError) as context:
            Product(id=1, name="Бракованный товар", price=-150.0)

        # Проверяем текст ошибки
        self.assertEqual(
            str(context.exception), "Цена товара не может быть отрицательной."
        )

    def test_product_creation_with_valid_price(self):
        """Проверка успешного создания товара с корректной (или нулевой) ценой."""
        product1 = Product(id=2, name="Хлеб", price=50.0)
        product2 = Product(id=3, name="Подарок", price=0.0)

        self.assertEqual(product1.price, 50.0)
        self.assertEqual(product2.price, 0.0)

    # --- Дополнительные тесты для проверки бизнес-логики ---
    def test_cart_totals_and_discounts(self):
        """Проверка корректности подсчета суммы и применения скидки через Декоратор."""
        cart = Cart()
        p1 = Product(1, "Смартфон", 800.0)
        p2 = Product(2, "Чехол", 300.0)

        cart.add_item(p1)
        cart.add_item(p2)

        # Проверяем базовую корзину (800 + 300 = 1100)
        self.assertEqual(cart.get_item_count(), 2)
        self.assertEqual(cart.get_total(), 1100.0)

        # Оборачиваем в сервис скидок
        discounted_cart = DiscountService(cart)

        # Сумма > 1000, ожидаем скидку 10% (1100 * 0.9 = 990)
        self.assertEqual(discounted_cart.get_total(), 990.0)


if __name__ == "__main__":
    unittest.main()