import os


class Encryptor:
    @staticmethod
    def encrypt(text: str, key: int) -> str:
        return "".join(chr(ord(char) ^ key) for char in text)

    @staticmethod
    def decrypt(encrypted: str, key: int) -> str:
        return "".join(chr(ord(char) ^ key) for char in encrypted)


class SecureStorage:
    def __init__(self, filename: str, encryptor: Encryptor):
        self.filename = filename
        self.encryptor = encryptor

    def save(self, text: str, key: int):
        try:
            encrypted_data = self.encryptor.encrypt(text, key)
            with open(self.filename, mode="w", encoding="utf-8") as f:
                f.write(encrypted_data)
        except PermissionError:
            print(f"Ошибка: Нет прав на запись в файл '{self.filename}'.")
        except OSError as e:
            if e.errno == 28:
                print(f"Ошибка: Недостаточно места на диске для файла '{self.filename}'.")
            else:
                print(f"Ошибка ввода-вывода при записи '{self.filename}': {e}")

    def load(self, key: int) -> str:
        try:
            if not os.path.exists(self.filename):
                print(f"Ошибка: Файл '{self.filename}' не найден.")
                return ""
            with open(self.filename, mode="r", encoding="utf-8") as f:
                encrypted_data = f.read()
            return self.encryptor.decrypt(encrypted_data, key)
        except PermissionError:
            print(f"Ошибка: Нет прав на чтение файла '{self.filename}'.")
            return ""
        except OSError as e:
            print(f"Ошибка ввода-вывода при чтении '{self.filename}': {e}")
            return ""


def test_encryption_correctness():
    encryptor = Encryptor()
    test_cases = [
        ("Hello, World!", 42),
        ("Python 2026", 123),
        ("", 5),
        ("СекретныйТекст123", 255),
        ("!@#$%^&*()_+", 17)
    ]

    print("Запуск тестов шифрования...")
    all_passed = True

    for text, key in test_cases:
        encrypted = encryptor.encrypt(text, key)
        decrypted = encryptor.decrypt(encrypted, key)
        
        if decrypted == text:
            print(f"Успешно: '{text}' (ключ {key}) -> '{encrypted.encode()}' -> '{decrypted}'")
        else:
            print(f"Ошибка: Для '{text}' (ключ {key}) получено '{decrypted}'")
            all_passed = False

    if all_passed:
        print("Все тесты успешно пройдены!\n")
    else:
        print("Обнаружены ошибки в тестах.\n")


if __name__ == "__main__":
    test_encryption_correctness()

    encryptor = Encryptor()
    storage = "secret.dat"
    secure_storage = SecureStorage(storage, encryptor)

    secret_key = 57
    original_text = "Важная информация для защиты"

    secure_storage.save(original_text, secret_key)
    decrypted_text = secure_storage.load(secret_key)

    print(f"Исходный текст: {original_text}")
    print(f"Восстановленный из файла текст: {decrypted_text}")