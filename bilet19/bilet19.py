import json
import os
import xml.etree.ElementTree as ET


class Product:
    def __init__(self, product_id: str, name: str, price: float):
        self.product_id = product_id
        self.name = name
        self.price = price

    def __repr__(self):
        return f"Product(id='{self.product_id}', name='{self.name}', price={self.price})"


class ProductCatalog:
    def __init__(self):
        self.products = {}

    def add_product(self, product: Product) -> bool:
        if product.product_id in self.products:
            print(f"[Catalog] Товар с ID {product.product_id} уже существует.")
            return False
        self.products[product.product_id] = product
        return True

    def get_all_products(self) -> list:
        return list(self.products.values())

    def find_by_id(self, product_id: str) -> Product:
        return self.products.get(product_id)


class JSONImporter:
    @staticmethod
    def import_products(filename: str, catalog: ProductCatalog):
        if not os.path.exists(filename):
            print(f"[JSON Import] Ошибка: Файл '{filename}' не найден.")
            return

        try:
            with open(filename, mode="r", encoding="utf-8") as f:
                data = json.load(f)

            if not isinstance(data, list):
                print(f"[JSON Import] Ошибка валидации: Корневой элемент должен быть списком.")
                return

            for index, item in enumerate(data):
                if not isinstance(item, dict):
                    print(f"[JSON Import] Ошибка: Элемент #{index} не является объектом.")
                    continue

                if "id" not in item or "name" not in item or "price" not in item:
                    print(f"[JSON Import] Ошибка валидации полей в элементе #{index}: {item}")
                    continue

                try:
                    product = Product(
                        product_id=str(item["id"]),
                        name=str(item["name"]),
                        price=float(item["price"])
                    )
                    catalog.add_product(product)
                except ValueError:
                    print(f"[JSON Import] Ошибка некорректного типа данных в элементе #{index}")

        except json.JSONDecodeError as e:
            print(f"[JSON Import] Критическая ошибка структуры файла. Неверный формат JSON: {e}")
        except PermissionError:
            print(f"[JSON Import] Ошибка доступа: Нет прав на чтение файла '{filename}'.")


class XMLImporter:
    @staticmethod
    def import_products(filename: str, catalog: ProductCatalog):
        if not os.path.exists(filename):
            print(f"[XML Import] Ошибка: Файл '{filename}' не найден.")
            return

        try:
            tree = ET.parse(filename)
            root = tree.getroot()

            for index, elem in enumerate(root.findall("product")):
                p_id = elem.find("id")
                name = elem.find("name")
                price = elem.find("price")

                if p_id is None or name is None or price is None:
                    print(f"[XML Import] Ошибка валидации: Пропущены обязательные теги в элементе #{index}")
                    continue

                try:
                    product = Product(
                        product_id=p_id.text.strip(),
                        name=name.text.strip(),
                        price=float(price.text.strip())
                    )
                    catalog.add_product(product)
                except (ValueError, AttributeError):
                    print(f"[XML Import] Ошибка при обработке значений данных элемента #{index}")

        except ET.ParseError as e:
            print(f"[XML Import] Критическая ошибка структуры файла. Неверный формат XML: {e}")
        except PermissionError:
            print(f"[XML Import] Ошибка доступа: Нет прав на чтение файла '{filename}'.")


if __name__ == "__main__":
    json_valid = "products_valid.json"
    json_invalid = "products_broken.json"
    xml_valid = "products_valid.xml"
    xml_invalid = "products_broken.xml"

    with open(json_valid, "w", encoding="utf-8") as f:
        f.write('[{"id": "101", "name": "Keyboard", "price": 1500.0}, {"id": "102", "name": "Mouse", "price": 800.0}]')

    with open(json_invalid, "w", encoding="utf-8") as f:
        f.write('[{"id": "103", "name": "Broken Item", "price": 500}, {строка_вызывающая_ошибку}]')

    with open(xml_valid, "w", encoding="utf-8") as f:
        f.write("<catalog><product><id>201</id><name>Monitor</name><price>12000</price></product>"
                "<product><id>202</id><name>RAM</name><price>3500</price></product></catalog>")

    with open(xml_invalid, "w", encoding="utf-8") as f:
        f.write("<catalog><product><id>203</id><price>400</price></product><unclosed_tag>")

    catalog = ProductCatalog()

    print("--- Тестирование импорта валидного JSON ---")
    JSONImporter.import_products(json_valid, catalog)

    print("\n--- Тестирование импорта поврежденного JSON (Отладка) ---")
    JSONImporter.import_products(json_invalid, catalog)

    print("\n--- Тестирование импорта валидного XML ---")
    XMLImporter.import_products(xml_valid, catalog)

    print("\n--- Тестирование импорта поврежденного XML (Отладка) ---")
    XMLImporter.import_products(xml_invalid, catalog)

    print("\n--- Итоговое содержимое каталога продуктов ---")
    for prod in catalog.get_all_products():
        print(f" Найдено в каталоге: {prod}")

    for file in [json_valid, json_invalid, xml_valid, xml_invalid]:
        if os.path.exists(file):
            os.remove(file)