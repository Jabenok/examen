import json
import os
import time


class Cache:
    def __init__(self):
        self.storage = {}

    def set(self, key: str, value: any, ttl: int):
        expire_at = time.time() + ttl
        self.storage[key] = {"value": value, "expire_at": expire_at}

    def get(self, key: str) -> any:
        self._cleanup()
        if key in self.storage:
            print(f"[CACHE HIT] Key: '{key}' found in cache.")
            return self.storage[key]["value"]
        
        print(f"[CACHE MISS] Key: '{key}' not found or expired.")
        return None

    def _cleanup(self):
        now = time.time()
        expired_keys = [k for k, v in self.storage.items() if now > v["expire_at"]]
        for k in expired_keys:
            del self.storage[k]


class CachedDataSource:
    def __init__(self, filename: str, cache: Cache):
        self.filename = filename
        self.cache = cache

    def get_data_by_id(self, record_id: str) -> dict:
        cache_key = f"record:{record_id}"
        cached_value = self.cache.get(cache_key)
        if cached_value is not None:
            return cached_value

        start_time = time.time()
        db_data = self._read_from_file_source(record_id)
        execution_time = time.time() - start_time
        
        print(f"[DB FETCH] Fetched from file source in {execution_time:.4f} seconds.")

        if db_data:
            self.cache.set(cache_key, db_data, ttl=5)
            
        return db_data

    def _read_from_file_source(self, record_id: str) -> dict:
        time.sleep(1.5)
        if not os.path.exists(self.filename):
            return {}
        try:
            with open(self.filename, mode="r", encoding="utf-8") as f:
                data = json.load(f)
                return data.get(record_id, {})
        except (json.JSONDecodeError, OSError):
            return {}


if __name__ == "__main__":
    mock_db = "mock_database.json"
    initial_data = {
        "101": {"name": "Laptop", "price": 1200},
        "102": {"name": "Smartphone", "price": 800}
    }
    
    with open(mock_db, mode="w", encoding="utf-8") as f:
        json.dump(initial_data, f)

    cache_system = Cache()
    data_source = CachedDataSource(mock_db, cache_system)

    print("--- Первый запрос (Промах кэша, чтение из 'БД') ---")
    start = time.time()
    res1 = data_source.get_data_by_id("101")
    print(f"Результат: {res1} | Время выполнения: {time.time() - start:.4f} сек\n")

    print("--- Второй запрос (Попадание в кэш) ---")
    start = time.time()
    res2 = data_source.get_data_by_id("101")
    print(f"Результат: {res2} | Время выполнения: {time.time() - start:.4f} сек\n")

    print("--- Ожидание 6 секунд для истечения срока TTL ---")
    time.sleep(6)

    print("--- Третий запрос после истечения TTL (Промах кэша) ---")
    start = time.time()
    res3 = data_source.get_data_by_id("101")
    print(f"Результат: {res3} | Время выполнения: {time.time() - start:.4f} сек\n")

    if os.path.exists(mock_db):
        os.remove(mock_db)