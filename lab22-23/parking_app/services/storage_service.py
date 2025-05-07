"""
Сервис для хранения и загрузки данных
"""

import os
import json
from typing import List, Dict, Any, Optional
from pathlib import Path
from models.car import Car


class StorageService:
    """Класс для работы с хранилищем данных"""

    def __init__(self, data_file: str = "parking_data.json"):
        """
        Инициализация сервиса хранения

        Args:
            data_file: Путь к файлу с данными
        """
        self.data_file = data_file
        self.data_path = Path(data_file)

    def load_data(self) -> List[Car]:
        """
        Загрузка данных из файла

        Returns:
            Список автомобилей
        """
        if not self.data_path.exists():
            return []

        try:
            with open(self.data_file, "r", encoding="utf-8") as file:
                data = json.load(file)
                return [Car.from_dict(car_data) for car_data in data]
        except (json.JSONDecodeError, KeyError) as e:
            print(f"Ошибка при чтении файла данных: {e}")
            # Создаем резервную копию поврежденного файла
            if self.data_path.exists():
                backup_file = f"{self.data_file}.bak"
                self.data_path.rename(backup_file)
                print(f"Создана резервная копия файла данных: {backup_file}")
            return []

    def save_data(self, cars: List[Car]) -> bool:
        """
        Сохранение данных в файл

        Args:
            cars: Список автомобилей для сохранения

        Returns:
            Успешность операции
        """
        try:
            # Создаем директорию, если её нет
            self.data_path.parent.mkdir(parents=True, exist_ok=True)

            # Преобразуем объекты в словари и сохраняем
            cars_data = [car.to_dict() for car in cars]

            # Сначала сохраняем во временный файл
            temp_file = f"{self.data_file}.tmp"
            with open(temp_file, "w", encoding="utf-8") as file:
                json.dump(cars_data, file, ensure_ascii=False, indent=4)

            # Если все в порядке, переименовываем временный файл
            Path(temp_file).rename(self.data_file)
            return True
        except Exception as e:
            print(f"Ошибка при сохранении данных: {e}")
            return False