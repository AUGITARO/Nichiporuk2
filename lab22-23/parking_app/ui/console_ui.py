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
