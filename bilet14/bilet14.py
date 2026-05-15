class Product:
    def __init__(self, name: str, category: str, price: float):
        self.name = name
        self.category = category
        self.price = price

    def __repr__(self):
        return f"Product(name='{self.name}', category='{self.category}', price={self.price})"


class SearchEngine:
    @staticmethod
    def search(items: list, query: str, field: str) -> list:
        if not query:
            return items
        
        result = []
        query_lower = query.lower()
        
        for item in items:
            if hasattr(item, field):
                value = getattr(item, field)
                if query_lower in str(value).lower():
                    result.append(item)
                    
        return result


class FilterEngine:
    def __init__(self, search_engine: SearchEngine):
        self.search_engine = search_engine

    def filter_and_search(self, items: list, query: str = None, search_field: str = None, 
                          category: str = None, price_min: float = None, price_max: float = None) -> list:
        
        if query and search_field:
            filtered_items = self.search_engine.search(items, query, search_field)
        else:
            filtered_items = items

        result = []
        for item in filtered_items:
            if category and getattr(item, "category", None) != category:
                continue
            if price_min is not None and getattr(item, "price", 0) < price_min:
                continue
            if price_max is not None and getattr(item, "price", 0) > price_max:
                continue
            result.append(item)

        return result


def test_price_range_filtration():
    print("--- Запуск тестов фильтрации по диапазону цен ---")
    search_eng = SearchEngine()
    filter_eng = FilterEngine(search_eng)

    products = [
        Product("Mouse", "Electronics", 50.0),
        Product("Keyboard", "Electronics", 150.0),
        Product("Monitor", "Electronics", 450.0),
        Product("Gaming Chair", "Furniture", 500.0),
        Product("Premium Desk", "Furniture", 600.0)
    ]

    print("Входные товары:")
    for p in products:
        print(f" - {p}")

    price_min, price_max = 100.0, 500.0
    print(f"\nФильтрация: цена от {price_min} до {price_max}")
    
    filtered = filter_eng.filter_and_search(products, price_min=price_min, price_max=price_max)
    
    expected_names = {"Keyboard", "Monitor", "Gaming Chair"}
    result_names = {p.name for p in filtered}

    print("Результат фильтрации:")
    for p in filtered:
        print(f" - {p}")

    if result_names == expected_names:
        print("\nТест фильтрации диапазона цен: УСПЕШНО")
    else:
        print(f"\nТест фильтрации диапазона цен: ОШИБКА (Ожидалось {expected_names}, получено {result_names})")


if __name__ == "__main__":
    test_price_range_filtration()

    print("\n--- Демонстрация совместной работы поиска и фильтрации ---")
    se = SearchEngine()
    fe = FilterEngine(se)

    catalog = [
        Product("Apple iPhone 14", "Smartphones", 800),
        Product("Samsung Galaxy S23", "Smartphones", 850),
        Product("Xiaomi Redmi Note 12", "Smartphones", 250),
        Product("Asus ROG Phone", "Smartphones", 990),
        Product("Apple iPad Air", "Tablets", 600)
    ]

    print("Поиск по запросу 'Apple' с фильтрацией цены до 700:")
    demo_res = fe.filter_and_search(
        items=catalog, 
        query="Apple", 
        search_field="name", 
        price_max=700
    )
    
    for product in demo_res:
        print(f" Найдено: {product}")