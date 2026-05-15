import time
from collections import deque
from threading import Lock, Thread


class MessageQueue:
    def __init__(self, max_size: int = 5):
        self.max_size = max_size
        self.queue = deque()
        self.lock = Lock()

    def push(self, message: str) -> bool:
        with self.lock:
            if len(self.queue) >= self.max_size:
                print(f"[Queue] Ошибка: Очередь переполнена. Не удалось добавить: '{message}'")
                return False
            self.queue.append(message)
            return True

    def pop(self) -> str:
        with self.lock:
            if not self.queue:
                return None
            return self.queue.popleft()

    def size(self) -> int:
        with self.lock:
            return len(self.queue)


class QueueProcessor:
    def __init__(self, message_queue: MessageQueue):
        self.message_queue = message_queue
        self.is_running = False

    def start(self):
        self.is_running = True
        self.worker = Thread(target=self._process_messages)
        self.worker.start()

    def stop(self):
        self.is_running = False
        if self.worker.is_alive():
            self.worker.join()

    def _process_messages(self):
        while self.is_running or self.message_queue.size() > 0:
            message = self.message_queue.pop()
            if message:
                print(f"[Processor] Обработано сообщение: {message}")
                time.sleep(0.5)
            else:
                time.sleep(0.1)


if __name__ == "__main__":
    queue = MessageQueue(max_size=3)
    processor = QueueProcessor(queue)

    print("--- Симуляция переполнения очереди ---")
    
    messages_to_push = ["Msg 1", "Msg 2", "Msg 3", "Msg 4", "Msg 5"]
    
    for msg in messages_to_push:
        success = queue.push(msg)
        if success:
            print(f"[Main] Успешно добавлено: {msg}")
        else:
            print(f"[Main] Система отклонила сообщение: {msg}")

    print(f"\nТекущий размер очереди перед обработкой: {queue.size()}")
    print("\n--- Запуск обработки сообщений ---")
    
    processor.start()
    
    while queue.size() > 0:
        time.sleep(0.1)
        
    processor.stop()
    print("\nВсе доступные сообщения из обработаны.")