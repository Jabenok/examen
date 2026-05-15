# Задание 1 (ПМ.01). Разработайте класс Database с
# методами connect(), execute_query(), close(). Создайте таблицу products (id,
# name, price, quantity).

# Задание 2 (ПМ.02). Реализуйте модуль ProductService с
# методами add_product(), get_all_products(), update_price().
# Используйте Database для выполнения SQL-запросов.

# Задание 3 (Отладка). Добавьте обработку ошибок SQL (нарушение
# уникальности, неверный тип данных). Продемонстрируйте rollback при
# ошибке в транзакции

import sqlite3 as sq



class Database:
    def __init__(self, db_name):
        self.db_name =  db_name
        self.connection = None

    def connect(self):
        try:
            self.connection = sq.connect(self.db_name)
            self.cursor = self.connection.cursor()
            self.cursor.execute('''CREATE TABLE IF NOT EXISTS products
                                (id INTEGER PRIMARY KEY AUTOINCREMENT,
                                 name TEXT NOT NULL,
                                 price REAL NOT NULL,
                                 quantity INTEGER NOT NULL)''')
            self.connection.commit()
        except sq.Error as e:
            print(f"Error connecting to database: {e}")
            if self.connection:
                self.connection.rollback()

    def execute_query(self, query, params=None):
        try:
            if params:
                self.cursor.execute(query, params)
            else:
                self.cursor.execute(query)
            self.connection.commit()
        except sq.Error as e:
            print(f"Error executing query: {e}")
            if self.connection:
                self.connection.rollback()
    
    def close(self):
        if self.connection:
            self.connection.close()


class ProductService:
    def __init__(self, db):
        self.db = db

    def add_product(self, name, price, quantity):
        query = "INSERT INTO products (name, price, quantity) VALUES (?, ?, ?)"
        self.db.execute_query(query, (name, price, quantity))

    def get_all_products(self):
        query = "SELECT * FROM products"
        self.db.cursor.execute(query)
        return self.db.cursor.fetchall()

    def update_price(self, product_id, new_price):
        query = "UPDATE products SET price = ? WHERE id = ?"
        self.db.execute_query(query, (new_price, product_id))



# Пример использования
if __name__ == "__main__":
    db = Database("products.db")
    db.connect()

    service = ProductService(db)
    service.add_product("Laptop", 999.99, 10)
    service.add_product("Smartphone", 499.99, 20)

    products = service.get_all_products()
    print("Products:", products)

    service.update_price(1, 899.99)
    updated_products = service.get_all_products()
    print("Updated Products:", updated_products)

    db.close()
