"""
Главный файл приложения "Автостоянка"
"""

import sys
from services.storage_service import StorageService
from services.parking_service import ParkingService
from ui.console_ui import ConsoleUI


def main():
    """Главная функция приложения"""
    print("Запуск приложения 'Автостоянка'...")

    try:
        # Инициализация сервисов
        storage_service = StorageService("data/parking_data.json")
        parking_service = ParkingService(storage_service)

        # Инициализация UI
        ui = ConsoleUI(parking_service)

        # Запуск главного меню
        ui.main_menu()

    except Exception as e:
        print(f"Произошла непредвиденная ошибка: {e}")
        return 1

    return 0


if __name__ == "__main__":
    sys.exit(main())