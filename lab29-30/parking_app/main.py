import sys
from services.storage_service import StorageService
from services.parking_service import ParkingService
from ui.gui_ui import ParkingGUI  # Импорт нового GUI

def main():
    print("Запуск приложения 'Автостоянка'...")

    try:
        storage_service = StorageService("data/parking_data.json")
        parking_service = ParkingService(storage_service)


        gui = ParkingGUI(parking_service)
        gui.run()

    except Exception as e:
        print(f"Произошла непредвиденная ошибка: {e}")
        return 1

    return 0

if __name__ == "main":
    sys.exit(main())