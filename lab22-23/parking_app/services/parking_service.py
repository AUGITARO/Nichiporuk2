from datetime import datetime
from typing import List, Dict, Any, Optional, Tuple
from models.car import Car
from services.storage_service import StorageService


class ParkingService:
    """Класс для управления автостоянкой"""

    def __init__(self, storage_service: StorageService):
        """
        Инициализация сервиса

        Args:
            storage_service: Сервис для работы с хранилищем данных
        """
        self.storage_service = storage_service
        self.cars = self.storage_service.load_data()

    def add_car(self, car_brand: str, car_number: str, owner_name: str,
                discount: int, hourly_rate: float = 100.0) -> Car:
        """
        Добавление автомобиля на стоянку

        Args:
            car_brand: Марка автомобиля
            car_number: Номер автомобиля
            owner_name: ФИО владельца
            discount: Скидка в процентах
            hourly_rate: Почасовая ставка

        Returns:
            Объект добавленного автомобиля
        """
        # Проверка на дубликаты
        for car in self.cars:
            if car.car_number == car_number and car.exit_time is None:
                raise ValueError(f"Автомобиль с номером {car_number} уже находится на стоянке")

        new_car = Car(
            car_brand=car_brand,
            car_number=car_number,
            owner_name=owner_name,
            entry_time=datetime.now(),
            hourly_rate=hourly_rate,
            discount=discount
        )

        self.cars.append(new_car)
        self.storage_service.save_data(self.cars)
        return new_car

    def remove_car(self, car_number: str) -> Tuple[Optional[Car], float]:
        """
        Вывод автомобиля со стоянки

        Args:
            car_number: Номер автомобиля

        Returns:
            Кортеж (автомобиль, стоимость)
        """
        for i, car in enumerate(self.cars):
            if car.car_number == car_number and car.exit_time is None:
                exit_time = datetime.now()
                self.cars[i].exit_time = exit_time

                cost = car.calculate_current_cost(exit_time)
                self.cars[i].cost = cost

                self.storage_service.save_data(self.cars)
                return self.cars[i], cost

        return None, 0.0

    def pay_for_parking(self, car_number: str) -> bool:
        """
        Оплата стоянки

        Args:
            car_number: Номер автомобиля

        Returns:
            Успешность операции
        """
        for i, car in enumerate(self.cars):
            if car.car_number == car_number and car.payment_status == "Не оплачено":
                self.cars[i].payment_status = "Оплачено"
                self.cars[i].debt = 0.0
                self.storage_service.save_data(self.cars)
                return True

        return False

    def get_current_cars(self) -> List[Car]:
        """
        Получение списка автомобилей на стоянке

        Returns:
            Список автомобилей на стоянке
        """
        return [car for car in self.cars if car.exit_time is None]

    def get_parking_history(self) -> List[Car]:
        """
        Получение истории стоянки

        Returns:
            Список автомобилей, которые были на стоянке
        """
        return [car for car in self.cars if car.exit_time is not None]

    def search_cars(self, search_term: str) -> List[Car]:
        """
        Поиск автомобилей

        Args:
            search_term: Строка поиска

        Returns:
            Список найденных автомобилей
        """
        search_term = search_term.lower()
        return [car for car in self.cars if (
                search_term in car.car_number.lower() or
                search_term in car.car_brand.lower() or
                search_term in car.owner_name.lower()
        )]

    def get_debtors(self) -> List[Car]:
        """
        Получение списка должников

        Returns:
            Список автомобилей с задолженностью
        """
        return [car for car in self.cars if car.payment_status == "Не оплачено" and car.debt > 0]

    def get_total_debt(self) -> float:
        """
        Расчет общей суммы задолженности

        Returns:
            Общая сумма задолженности
        """
        return sum(car.debt for car in self.cars if car.payment_status == "Не оплачено")

    def update_car_debt(self, car_number: str, cost: float) -> bool:
        """
        Обновление задолженности автомобиля

        Args:
            car_number: Номер автомобиля
            cost: Сумма задолженности

        Returns:
            Успешность операции
        """
        for i, car in enumerate(self.cars):
            if car.car_number == car_number:
                self.cars[i].debt = cost
                self.storage_service.save_data(self.cars)
                return True

        return False
