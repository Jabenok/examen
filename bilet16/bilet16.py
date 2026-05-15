import json
import time


class APIClient:
    def __init__(self, timeout: int = 5):
        self.timeout = timeout

    def get(self, url: str) -> dict:
        print(f"[APIClient] Выполнение GET-запроса к '{url}'...")
        
        # Симуляция сетевых задержек и ошибок на основе URL для тестирования отладки
        if "timeout_demo" in url:
            time.sleep(self.timeout + 0.5)
            raise TimeoutError(f"Превышено время ожидания ответа от сервера ({self.timeout} сек).")
            
        if "server_error_demo" in url:
            raise ConnectionError("Сервер недоступен или не отвечает на запросы.")

        # Эмуляция успешного ответа сервера (Mock JSON)
        if "weather" in url:
            mock_json_response = '{"status": "success", "data": {"city": "Moscow", "temperature": 18, "condition": "Sunny"}}'
        else:
            mock_json_response = '{"status": "success", "message": "Connection established"}'

        try:
            data = json.loads(mock_json_response)
            return data
        except json.JSONDecodeError:
            print("[APIClient] Ошибка: Некорректный формат JSON в ответе сервера.")
            return {}


class WeatherService:
    def __init__(self, api_client: APIClient):
        self.api_client = api_client
        self.base_url = "https://api.mockweather.local/v1"

    def get_temperature(self, city: str) -> float:
        url = f"{self.base_url}/weather?q={city}"
        try:
            response = self.api_client.get(url)
            
            if response.get("status") == "success":
                data = response.get("data", {})
                temperature = data.get("temperature")
                return float(temperature)
            else:
                print(f"[WeatherService] Не удалось получить данные о погоде: {response.get('message')}")
                return None
                
        except TimeoutError as e:
            print(f"[Пользовательское сообщение] Ошибка сети: {e} Пожалуйста, проверьте соединение или попробуйте позже.")
            return None
        except ConnectionError as e:
            print(f"[Пользовательское сообщение] Критическая ошибка: {e} Удаленный сервер временно не принимает запросы.")
            return None
        except Exception as e:
            print(f"[Пользовательское сообщение] Непредвиденная ошибка при работе с API: {e}")
            return None


if __name__ == "__main__":
    client = APIClient(timeout=3)
    weather_service = WeatherService(client)

    print("--- Тест 1: Успешный запрос данных о погоде ---")
    temp = weather_service.get_temperature("Moscow")
    if temp is not None:
        print(f"Результат: Температура в городе составляет {temp}°C\n")

    print("--- Тест 2: Отладка обработки таймаута сети ---")
    weather_service.base_url = "https://api.timeout_demo.local/v1"
    weather_service.get_temperature("Moscow")
    print()

    print("--- Тест 3: Отладка обработки недоступности сервера ---")
    weather_service.base_url = "https://api.server_error_demo.local/v1"
    weather_service.get_temperature("Moscow")