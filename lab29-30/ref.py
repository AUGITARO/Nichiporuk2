# Структура проекта после рефакторинга:
#
# parking_app/
# ├── main.py                  # Главный файл запуска приложения
# ├── models/                  # Модели данных
# │   ├── __init__.py
# │   └── car.py               # Класс автомобиля
# ├── services/                # Бизнес-логика
# │   ├── __init__.py
# │   ├── parking_service.py   # Сервис управления автостоянкой
# │   └── storage_service.py   # Сервис хранения данных
# ├── utils/                   # Утилиты
# │   ├── __init__.py
# │   └── helpers.py           # Вспомогательные функции
# └── ui/                      # Пользовательский интерфейс
#     ├── __init__.py
#     └── console_ui.py        # Консольный интерфейс
#
# Ниже представлено содержимое каждого файла

# -------------------------------------------
# models/__init__.py
# -------------------------------------------
"""
Пакет с моделями данных для приложения "Автостоянка"
"""

# -------------------------------------------
# models/car.py
# -------------------------------------------
"""
Модель данных для представления автомобиля на стоянке
"""

from datetime import datetime
from dataclasses import dataclass, field
from typing import Optional


@dataclass
class Car:
    """Класс для представления автомобиля на стоянке"""
    car_brand: str
    car_number: str
    owner_name: str
    entry_time: datetime
    hourly_rate: float
    discount: int
    exit_time: Optional[datetime] = None
    payment_status: str = "Не оплачено"
    debt: float = 0.0
    cost: float = 0.0
    id: str = field(default_factory=lambda: datetime.now().strftime("%Y%m%d%H%M%S"))

    def calculate_current_cost(self, current_time: datetime = None) -> float:
        """Расчет текущей стоимости стоянки"""
        if current_time is None:
            current_time = datetime.now()

        if self.exit_time is not None:
            end_time = self.exit_time
        else:
            end_time = current_time

        time_diff = end_time - self.entry_time
        hours = time_diff.total_seconds() / 3600
        cost = hours * self.hourly_rate
        discount_amount = cost * (self.discount / 100)
        final_cost = cost - discount_amount
        return max(0, round(final_cost, 2))

    def get_duration(self, current_time: datetime = None) -> float:
        """Расчет длительности пребывания на стоянке в часах"""
        if current_time is None:
            current_time = datetime.now()

        if self.exit_time is not None:
            end_time = self.exit_time
        else:
            end_time = current_time

        time_diff = end_time - self.entry_time
        return round(time_diff.total_seconds() / 3600, 2)

    def to_dict(self) -> dict:
        """Преобразование объекта в словарь для сохранения"""
        return {
            "id": self.id,
            "car_brand": self.car_brand,
            "car_number": self.car_number,
            "owner_name": self.owner_name,
            "entry_time": self.entry_time.isoformat(),
            "hourly_rate": self.hourly_rate,
            "discount": self.discount,
            "exit_time": self.exit_time.isoformat() if self.exit_time else None,
            "payment_status": self.payment_status,
            "debt": self.debt,
            "cost": self.cost
        }

    @classmethod
    def from_dict(cls, data: dict) -> 'Car':
        """Создание объекта из словаря"""
        car = cls(
            car_brand=data["car_brand"],
            car_number=data["car_number"],
            owner_name=data["owner_name"],
            entry_time=datetime.fromisoformat(data["entry_time"]),
            hourly_rate=data["hourly_rate"],
            discount=data["discount"],
            payment_status=data["payment_status"],
            debt=data["debt"],
            id=data.get("id", datetime.now().strftime("%Y%m%d%H%M%S"))
        )

        if data["exit_time"]:
            car.exit_time = datetime.fromisoformat(data["exit_time"])

        if "cost" in data:
            car.cost = data["cost"]

        return car


# -------------------------------------------
# services/__init__.py
# -------------------------------------------
"""
Пакет с сервисами для приложения "Автостоянка"
"""

# -------------------------------------------
# services/storage_service.py
# -------------------------------------------
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


# -------------------------------------------
# services/parking_service.py
# -------------------------------------------
"""
Сервис управления автостоянкой
"""

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


# -------------------------------------------
# utils/__init__.py
# -------------------------------------------
"""
Пакет с утилитами для приложения "Автостоянка"
"""

# -------------------------------------------
# utils/helpers.py
# -------------------------------------------
"""
Вспомогательные функции для приложения
"""

from datetime import datetime, timedelta
from typing import Optional, Union


def validate_numeric_input(value: str, min_value: float = None, max_value: float = None) -> Optional[float]:
    """
    Проверка числового ввода

    Args:
        value: Строка для проверки
        min_value: Минимальное значение
        max_value: Максимальное значение

    Returns:
        Числовое значение или None в случае ошибки
    """
    try:
        numeric_value = float(value)

        if min_value is not None and numeric_value < min_value:
            print(f"Ошибка: значение должно быть не меньше {min_value}")
            return None

        if max_value is not None and numeric_value > max_value:
            print(f"Ошибка: значение должно быть не больше {max_value}")
            return None

        return numeric_value
    except ValueError:
        print("Ошибка: введите корректное числовое значение")
        return None


def format_time_difference(time1: datetime, time2: datetime) -> str:
    """
    Форматирование разницы между двумя моментами времени

    Args:
        time1: Первый момент времени
        time2: Второй момент времени

    Returns:
        Строка с отформатированной разницей
    """
    diff = abs(time2 - time1)
    days = diff.days
    hours, remainder = divmod(diff.seconds, 3600)
    minutes, seconds = divmod(remainder, 60)

    result = []
    if days > 0:
        result.append(f"{days} д.")
    if hours > 0 or days > 0:
        result.append(f"{hours} ч.")
    if minutes > 0 or hours > 0 or days > 0:
        result.append(f"{minutes} мин.")
    if not result:
        result.append(f"{seconds} сек.")

    return " ".join(result)


def format_money(amount: float) -> str:
    """
    Форматирование денежной суммы

    Args:
        amount: Сумма

    Returns:
        Отформатированная строка
    """
    return f"{amount:.2f} руб."


def get_yes_no_input(prompt: str) -> bool:
    """
    Получение ответа да/нет

    Args:
        prompt: Приглашение к вводу

    Returns:
        True если ответ "да", False в противном случае
    """
    response = input(f"{prompt} (да/нет): ").lower().strip()
    return response in ("да", "y", "yes", "д")


# -------------------------------------------
# ui/__init__.py
# -------------------------------------------
"""
Пакет с пользовательским интерфейсом для приложения "Автостоянка"
"""

# -------------------------------------------
# ui/console_ui.py
# -------------------------------------------
"""
Консольный интерфейс для приложения "Автостоянка"
"""

import os
from datetime import datetime
from typing import List, Optional
from models.car import Car
from services.parking_service import ParkingService
from utils.helpers import validate_numeric_input, format_time_difference, format_money, get_yes_no_input


class ConsoleUI:
    """Класс консольного интерфейса приложения"""

    def __init__(self, parking_service: ParkingService):
        """
        Инициализация UI

        Args:
            parking_service: Сервис управления автостоянкой
        """
        self.parking_service = parking_service

    def clear_screen(self):
        """Очистка экрана консоли"""
        os.system('cls' if os.name == 'nt' else 'clear')

    def print_header(self, title: str):
        """
        Вывод заголовка

        Args:
            title: Заголовок
        """
        self.clear_screen()
        print(f"\n{'=' * 50}")
        print(f"{title.center(50)}")
        print(f"{'=' * 50}\n")

    def add_car(self):
        """Добавление автомобиля на стоянку"""
        self.print_header("ДОБАВЛЕНИЕ АВТОМОБИЛЯ НА СТОЯНКУ")

        car_brand = input("Введите марку автомобиля: ").strip()
        if not car_brand:
            print("Ошибка: марка автомобиля не может быть пустой")
            input("Нажмите Enter для продолжения...")
            return

        car_number = input("Введите номер автомобиля: ").strip().upper()
        if not car_number:
            print("Ошибка: номер автомобиля не может быть пустым")
            input("Нажмите Enter для продолжения...")
            return

        owner_name = input("Введите ФИО владельца: ").strip()
        if not owner_name:
            print("Ошибка: ФИО владельца не может быть пустым")
            input("Нажмите Enter для продолжения...")
            return

        discount_input = input("Введите скидку в процентах (0-100): ").strip()
        discount = validate_numeric_input(discount_input, 0, 100)
        if discount is None:
            input("Нажмите Enter для продолжения...")
            return

        hourly_rate_input = input("Введите почасовую ставку (по умолчанию 100 руб.): ").strip()
        if hourly_rate_input:
            hourly_rate = validate_numeric_input(hourly_rate_input, 1)
            if hourly_rate is None:
                input("Нажмите Enter для продолжения...")
                return
        else:
            hourly_rate = 100.0

        try:
            car = self.parking_service.add_car(
                car_brand=car_brand,
                car_number=car_number,
                owner_name=owner_name,
                discount=int(discount),
                hourly_rate=hourly_rate
            )
            print(f"\nАвтомобиль {car.car_brand} {car.car_number} успешно добавлен на стоянку.")
            print(f"Время въезда: {car.entry_time.strftime('%d.%m.%Y %H:%M:%S')}")
            print(f"Почасовая ставка: {format_money(car.hourly_rate)}")
            if car.discount > 0:
                print(f"Скидка: {car.discount}%")
        except ValueError as e:
            print(f"Ошибка: {e}")

        input("\nНажмите Enter для продолжения...")

    def remove_car(self):
        """Вывод автомобиля со стоянки"""
        self.print_header("ВЫВОД АВТОМОБИЛЯ СО СТОЯНКИ")

        car_number = input("Введите номер автомобиля для вывода: ").strip().upper()
        if not car_number:
            print("Ошибка: номер автомобиля не может быть пустым")
            input("Нажмите Enter для продолжения...")
            return

        car, cost = self.parking_service.remove_car(car_number)

        if car is None:
            print("Автомобиль с таким номером не найден на стоянке или уже выведен.")
            input("Нажмите Enter для продолжения...")
            return

        print(f"\nАвтомобиль {car.car_brand} {car.car_number} выведен со стоянки.")
        print(f"Владелец: {car.owner_name}")
        print(f"Время въезда: {car.entry_time.strftime('%d.%m.%Y %H:%M:%S')}")
        print(f"Время выезда: {car.exit_time.strftime('%d.%m.%Y %H:%M:%S')}")
        print(f"Время пребывания: {format_time_difference(car.entry_time, car.exit_time)}")
        print(f"Стоимость стоянки: {format_money(cost)}")

        if get_yes_no_input("\nЖелаете оплатить стоянку сейчас?"):
            self.parking_service.pay_for_parking(car_number)
            print("Стоянка оплачена. Спасибо!")
        else:
            self.parking_service.update_car_debt(car_number, cost)
            print(f"Задолженность: {format_money(cost)}")

        input("\nНажмите Enter для продолжения...")

    def show_current_cars(self):
        """Просмотр текущих автомобилей на стоянке"""
        self.print_header("АВТОМОБИЛИ НА СТОЯНКЕ")

        current_cars = self.parking_service.get_current_cars()

        if not current_cars:
            print("На стоянке нет автомобилей.")
            input("\nНажмите Enter для продолжения...")
            return

        now = datetime.now()
        print(f"Всего автомобилей на стоянке: {len(current_cars)}\n")

        for i, car in enumerate(current_cars, 1):
            duration = format_time_difference(car.entry_time, now)
            current_cost = car.calculate_current_cost(now)

            print(f"{i}. Марка: {car.car_brand}, Номер: {car.car_number}")
            print(f"   Владелец: {car.owner_name}")
            print(f"   Время въезда: {car.entry_time.strftime('%d.%m.%Y %H:%M:%S')}")
            print(f"   Длительность пребывания: {duration}")
            print(f"   Текущая стоимость: {format_money(current_cost)}")
            print(f"   Почасовая ставка: {format_money(car.hourly_rate)}")
            if car.discount > 0:
                print(f"   Скидка: {car.discount}%")
            print("-" * 50)

        input("\nНажмите Enter для продолжения...")

    def show_history(self):
        """Просмотр истории стоянки"""
        self.print_header("ИСТОРИЯ СТОЯНКИ")

        history = self.parking_service.get_parking_history()

        if not history:
            print("История пуста.")
            input("\nНажмите Enter для продолжения...")
            return

        print(f"Всего записей: {len(history)}\n")

        for i, car in enumerate(sorted(history, key=lambda x: x.exit_time, reverse=True), 1):
            duration = format_time_difference(car.entry_time, car.exit_time)

            print(f"{i}. Марка: {car.car_brand}, Номер: {car.car_number}")
            print(f"   Владелец: {car.owner_name}")
            print(f"   Время въезда: {car.entry_time.strftime('%d.%m.%Y %H:%M:%S')}")
            print(f"   Время выезда: {car.exit_time.strftime('%d.%m.%Y %H:%M:%S')}")
            print(f"   Длительность пребывания: {duration}")
            print(f"   Стоимость: {format_money(car.cost)}")
            if car.discount > 0:
                print(f"   Скидка: {car.discount}%")
            print(f"   Статус оплаты: {car.payment_status}")
            if car.payment_status == "Не оплачено":
                print(f"   Задолженность: {format_money(car.debt)}")
            print("-" * 50)

        input("\nНажмите Enter для продолжения...")

    def search_car(self):
        """Поиск автомобиля"""
        self.print_header("ПОИСК АВТОМОБИЛЯ")

        search_term = input("Введите номер, марку автомобиля или ФИО владельца: ").strip()
        if not search_term:
            print("Ошибка: поисковый запрос не может быть пустым")
            input("Нажмите Enter для продолжения...")
            return

        found_cars = self.parking_service.search_cars(search_term)

        if not found_cars:
            print("Автомобили не найдены.")
            input("\nНажмите Enter для продолжения...")
            return

        print(f"Найдено автомобилей: {len(found_cars)}\n")

        for i, car in enumerate(found_cars, 1):
            print(f"{i}. Марка: {car.car_brand}, Номер: {car.car_number}")
            print(f"   Владелец: {car.owner_name}")
            print(f"   Время въезда: {car.entry_time.strftime('%d.%m.%Y %H:%M:%S')}")

            if car.exit_time is not None:
                print(f"   Время выезда: {car.exit_time.strftime('%d.%m.%Y %H:%M:%S')}")
                print(f"   Длительность пребывания: {format_time_difference(car.entry_time, car.exit_time)}")
                print(f"   Стоимость: {format_money(car.cost)}")
                print(f"   Статус оплаты: {car.payment_status}")
                if car.payment_status == "Не оплачено":
                    print(f"   Задолженность: {format_money(car.debt)}")
            else:
                now = datetime.now()
                duration = format_time_difference(car.entry_time, now)
                current_cost = car.calculate_current_cost(now)
                print(f"   Статус: На стоянке")
                print(f"   Текущая длительность: {duration}")
                print(f"   Текущая стоимость: {format_money(current_cost)}")

            print("-" * 50)

        input("\nНажмите Enter для продолжения...")

    def pay_debt(self):
        """Оплата задолженности"""
        self.print_header("ОПЛАТА ЗАДОЛЖЕННОСТИ")

        car_number = input("Введите номер автомобиля для оплаты задолженности: ").strip().upper()
        if not car_number:
            print("Ошибка: номер автомобиля не может быть пустым")
            input("Нажмите Enter для продолжения...")
            return

        found_cars = self.parking_service.search_cars(car_number)
        debtors = [car for car in found_cars if car.payment_status == "Не оплачено" and car.debt > 0]

        if not debtors:
            print("Автомобиль с таким номером не найден или нет задолженности.")
            input("\nНажмите Enter для продолжения...")
            return

        for car in debtors:
            print(f"\nАвтомобиль: {car.car_brand} {car.car_number}")
            print(f"Владелец: {car.owner_name}")
            print(f"Задолженность: {format_money(car.debt)}")

            if get_yes_no_input("Подтвердите оплату"):
                if self.parking_service.pay_for_parking(car.car_number):
                    print("Оплата прошла успешно. Спасибо!")
                else:
                    print("Произошла ошибка при оплате.")

        input("\nНажмите Enter для продолжения...")

    def show_debtors(self):
        """Просмотр должников"""
        self.print_header("СПИСОК ДОЛЖНИКОВ")

        debtors = self.parking_service.get_debtors()

        if not debtors:
            print("Должников нет.")
            input("\nНажмите Enter для продолжения...")
            return

        total_debt = self.parking_service.get_total_debt()
        print(f"Общая сумма задолженности: {format_money(total_debt)}\n")
        print(f"Всего должников: {len(debtors)}\n")

        for i, car in enumerate(debtors, 1):
            print(f"{i}. Марка: {car.car_brand}, Номер: {car.car_number}")
            print(f"   Владелец: {car.owner_name}")
            print(f"   Задолженность: {format_money(car.debt)}")
            print("-" * 50)

        input("\nНажмите Enter для продолжения...")

    def show_statistics(self):
        """Просмотр статистики"""
        self.print_header("СТАТИСТИКА АВТОСТОЯНКИ")

        current_cars = self.parking_service.get_current_cars()
        history = self.parking_service.get_parking_history()
        debtors = self.parking_service.get_debtors()
        total_debt = self.parking_service.get_total_debt()

        print(f"Автомобилей на стоянке: {len(current_cars)}")
        print(f"Всего обслужено автомобилей: {len(history)}")
        print(f"Количество должников: {len(debtors)}")
        print(f"Общая сумма задолженности: {format_money(total_debt)}")

        if history:
            total_revenue = sum(car.cost for car in history if car.payment_status == "Оплачено")
            print(f"Общая выручка: {format_money(total_revenue)}")

            total_expected = sum(car.cost for car in history)
            print(f"Ожидаемая выручка: {format_money(total_expected)}")

        input("\nНажмите Enter для продолжения...")

    def main_menu(self):
        """Главное меню приложения"""
        while True:
            self.print_header("АВТОСТОЯНКА")

            print("1. Добавить автомобиль на стоянку")
            print("2. Вывести автомобиль со стоянки")
            print("3. Показать текущие автомобили на стоянке")
            print("4. Просмотреть историю стоянки")
            print("5. Поиск автомобиля")
            print("6. Оплата задолженности")
            print("7. Просмотр должников")
            print("8. Статистика")
            print("0. Выход")

            choice = input("\nВыберите действие: ").strip()

            if choice == "1":
                self.add_car()
            elif choice == "2":
                self.remove_car()
            elif choice == "3":
                self.show_current_cars()
            elif choice == "4":
                self.show_history()
            elif choice == "5":
                self.search_car()
            elif choice == "6":
                self.pay_debt()
            elif choice == "7":
                self.show_debtors()
            elif choice == "8":
                self.show_statistics()
            elif choice == "0":
                self.print_header("ВЫХОД")
                print("Спасибо за использование программы!")
                break
            else:
                print("Неверный ввод. Попробуйте снова.")
                input("Нажмите Enter для продолжения...")


# -------------------------------------------
# main.py
# -------------------------------------------
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