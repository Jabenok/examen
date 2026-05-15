import os
import shutil
from datetime import datetime


class BackupManager:
    @staticmethod
    def create_backup(source_dir: str, dest_dir: str) -> str:
        if not os.path.exists(source_dir):
            print(f"[Backup] Ошибка: Исходная директория '{source_dir}' не существует.")
            return ""

        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        backup_folder_name = f"backup_{timestamp}"
        target_path = os.path.join(dest_dir, backup_folder_name)

        try:
            if not os.path.exists(dest_dir):
                print(f"[Backup] Предупреждение: Целевая директория '{dest_dir}' не существует. Попытка создания...")
                os.makedirs(dest_dir)

            shutil.copytree(source_dir, target_path)
            print(f"[Backup] Резервная копия успешно создана в: '{target_path}'")
            return target_path

        except PermissionError:
            print(f"[Backup] Ошибка: Нет прав на запись в целевую директорию '{dest_dir}'.")
            return ""
        except OSError as e:
            if e.errno == 28:
                print(f"[Backup] Ошибка: Недостаточно места на диске для создания бэкапа.")
            else:
                print(f"[Backup] Ошибка системы при копировании: {e}")
            return ""


class RestoreManager:
    def __init__(self, backup_manager: BackupManager):
        self.backup_manager = backup_manager

    @staticmethod
    def restore(backup_dir: str, restore_to_dir: str) -> bool:
        if not os.path.exists(backup_dir):
            print(f"[Restore] Ошибка: Директория бэкапа '{backup_dir}' не существует.")
            return False

        try:
            if os.path.exists(restore_to_dir):
                shutil.rmtree(restore_to_dir)
            
            shutil.copytree(backup_dir, restore_to_dir)
            print(f"[Restore] Данные успешно восстановлены из '{backup_dir}' в '{restore_to_dir}'")
            return True

        except PermissionError:
            print(f"[Restore] Ошибка: Нет прав на чтение из '{backup_dir}' или запись в '{restore_to_dir}'.")
            return False
        except OSError as e:
            print(f"[Restore] Ошибка системы при восстановлении данных: {e}")
            return False


if __name__ == "__main__":
    src = "source_data"
    dst = "backup_storage"
    restored = "restored_data"

    os.makedirs(src, exist_ok=True)
    with open(os.path.join(src, "config.txt"), "w", encoding="utf-8") as f:
        f.write("important_system_settings=True")
    with open(os.path.join(src, "data.db"), "w", encoding="utf-8") as f:
        f.write("user_records_payload")

    print("--- Демонстрация создания резервной копии ---")
    bm = BackupManager()
    backup_result_dir = bm.create_backup(src, dst)

    if backup_result_dir:
        print("\n--- Демонстрация восстановления данных ---")
        rm = RestoreManager(bm)
        rm.restore(backup_result_dir, restored)

    print("\n--- Симуляция ошибок (ПМ.03 Отладка) ---")
    print("1. Исходная директория не существует:")
    bm.create_backup("non_existent_folder", dst)

    print("\n2. Ошибка отсутствия прав доступа (имитация через некорректный путь):")
    bm.create_backup(src, "/sys/invalid_permission_path_demo")

    for folder in [src, dst, restored]:
        if os.path.exists(folder):
            shutil.rmtree(folder)