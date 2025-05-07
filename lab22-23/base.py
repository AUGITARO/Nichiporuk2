import os
import json
import datetime
from typing import List, Dict, Any

# Глобальные переменные
data_file = "parking_data.json"
cars_data = []

# Определение начальной структуры данных
if os.path.exists(data_file):
    with open(data_file, "r", encoding="utf-8") as file:
        cars_data = json.load(file)
else:
    cars_data = []


# Функция сохранения данных в файл
def save_data():
    with open(data_file, "w", encoding="utf-8") as file:
        json.dump(cars_data, file, ensure_ascii=False, indent=4, default=str)


# Функция добавления автомобиля на стоянку
def add_car():
    print("\n=== Добавление автомобиля на стоянку ===")
    car_brand = input("Введите марку автомобиля: ")
    car_number = input("Введите номер автомобиля: ")
    owner_name = input("Введите ФИО владельца: ")
    discount = input("Введите скидку в процентах (0-100): ")

    try:
        discount = int(discount)
        if discount < 0 or discount > 100:
            print("Ошибка: скидка должна быть от 0 до 100%")
            return
    except ValueError:
        print("Ошибка: введите числовое значение для скидки")
        return

    entry_time = datetime.datetime.now()

    # Расчет стоимости (базовая ставка 100 руб/час)
    hourly_rate = 100

    car = {
        "car_brand": car_brand,
        "car_number": car_number,
        "owner_name": owner_name,
        "entry_time": entry_time,
        "hourly_rate": hourly_rate,
        "discount": discount,
        "exit_time": None,
        "payment_status": "Не оплачено",
        "debt": 0.0
    }

    cars_data.append(car)
    save_data()
    print(f"Автомобиль {car_brand} {car_number} добавлен на стоянку.")


# Функция расчета стоимости стоянки
def calculate_cost(entry_time, exit_time, hourly_rate, discount):
    time_diff = exit_time - entry_time
    hours = time_diff.total_seconds() / 3600
    cost = hours * hourly_rate
    discount_amount = cost * (discount / 100)
    final_cost = cost - discount_amount
    return max(0, round(final_cost, 2))


# Функция вывода автомобиля со стоянки
def remove_car():
    print("\n=== Вывод автомобиля со стоянки ===")
    car_number = input("Введите номер автомобиля для вывода: ")

    for i, car in enumerate(cars_data):
        if car["car_number"] == car_number and car["exit_time"] is None:
            exit_time = datetime.datetime.now()
            cost = calculate_cost(
                datetime.datetime.fromisoformat(str(car["entry_time"])) if isinstance(car["entry_time"], str) else car[
                    "entry_time"],
                exit_time,
                car["hourly_rate"],
                car["discount"]
            )

            cars_data[i]["exit_time"] = exit_time
            cars_data[i]["cost"] = cost

            print(f"Автомобиль {car['car_brand']} {car_number} выведен со стоянки.")
            print(
                f"Время пребывания: {exit_time - (datetime.datetime.fromisoformat(str(car['entry_time'])) if isinstance(car['entry_time'], str) else car['entry_time'])}")
            print(f"Стоимость стоянки: {cost} руб.")

            payment = input("Желаете оплатить стоянку сейчас? (да/нет): ")
            if payment.lower() == "да":
                cars_data[i]["payment_status"] = "Оплачено"
                print("Стоянка оплачена. Спасибо!")
            else:
                cars_data[i]["payment_status"] = "Не оплачено"
                cars_data[i]["debt"] = cost
                print(f"Задолженность: {cost} руб.")

            save_data()
            return

    print("Автомобиль с таким номером не найден на стоянке или уже выведен.")


# Функция оплаты задолженности
def pay_debt():
    print("\n=== Оплата задолженности ===")
    car_number = input("Введите номер автомобиля для оплаты задолженности: ")

    for i, car in enumerate(cars_data):
        if car["car_number"] == car_number and car["payment_status"] == "Не оплачено":
            print(f"Задолженность за стоянку: {car['debt']} руб.")
            payment = input("Подтвердите оплату (да/нет): ")
            if payment.lower() == "да":
                cars_data[i]["payment_status"] = "Оплачено"
                cars_data[i]["debt"] = 0.0
                save_data()
                print("Оплата прошла успешно. Спасибо!")
            return

    print("Автомобиль с таким номером не найден или нет задолженности.")


# Функция просмотра автомобилей на стоянке
def show_current_cars():
    print("\n=== Автомобили на стоянке ===")
    current_cars = [car for car in cars_data if car["exit_time"] is None]

    if not current_cars:
        print("На стоянке нет автомобилей.")
        return

    for i, car in enumerate(current_cars, 1):
        entry_time = datetime.datetime.fromisoformat(str(car["entry_time"])) if isinstance(car["entry_time"], str) else \
        car["entry_time"]
        now = datetime.datetime.now()
        duration = now - entry_time
        hours = duration.total_seconds() / 3600
        current_cost = calculate_cost(entry_time, now, car["hourly_rate"], car["discount"])

        print(f"{i}. Марка: {car['car_brand']}, Номер: {car['car_number']}")
        print(f"   Владелец: {car['owner_name']}")
        print(f"   Время въезда: {entry_time}")
        print(f"   Текущая длительность: {round(hours, 2)} ч.")
        print(f"   Текущая стоимость: {current_cost} руб.")
        print(f"   Скидка: {car['discount']}%")
        print("-" * 40)


# Функция просмотра истории стоянки
def show_history():
    print("\n=== История стоянки ===")
    history_cars = [car for car in cars_data if car["exit_time"] is not None]

    if not history_cars:
        print("История пуста.")
        return

    for i, car in enumerate(history_cars, 1):
        entry_time = datetime.datetime.fromisoformat(str(car["entry_time"])) if isinstance(car["entry_time"], str) else \
        car["entry_time"]
        exit_time = datetime.datetime.fromisoformat(str(car["exit_time"])) if isinstance(car["exit_time"], str) else \
        car["exit_time"]
        duration = exit_time - entry_time
        hours = duration.total_seconds() / 3600

        print(f"{i}. Марка: {car['car_brand']}, Номер: {car['car_number']}")
        print(f"   Владелец: {car['owner_name']}")
        print(f"   Время въезда: {entry_time}")
        print(f"   Время выезда: {exit_time}")
        print(f"   Длительность: {round(hours, 2)} ч.")
        print(f"   Стоимость: {car.get('cost', 0)} руб.")
        print(f"   Скидка: {car['discount']}%")
        print(f"   Статус оплаты: {car['payment_status']}")
        if car['payment_status'] == "Не оплачено":
            print(f"   Задолженность: {car['debt']} руб.")
        print("-" * 40)


# Функция поиска автомобиля
def search_car():
    print("\n=== Поиск автомобиля ===")
    search_term = input("Введите номер или марку автомобиля: ").lower()

    found_cars = []
    for car in cars_data:
        if (search_term in car["car_number"].lower() or
                search_term in car["car_brand"].lower() or
                search_term in car["owner_name"].lower()):
            found_cars.append(car)

    if not found_cars:
        print("Автомобили не найдены.")
        return

    print(f"Найдено автомобилей: {len(found_cars)}")
    for i, car in enumerate(found_cars, 1):
        entry_time = datetime.datetime.fromisoformat(str(car["entry_time"])) if isinstance(car["entry_time"], str) else \
        car["entry_time"]
        print(f"{i}. Марка: {car['car_brand']}, Номер: {car['car_number']}")
        print(f"   Владелец: {car['owner_name']}")
        print(f"   Время въезда: {entry_time}")

        if car["exit_time"] is not None:
            exit_time = datetime.datetime.fromisoformat(str(car["exit_time"])) if isinstance(car["exit_time"], str) else \
            car["exit_time"]
            print(f"   Время выезда: {exit_time}")
            print(f"   Статус оплаты: {car['payment_status']}")
            if car['payment_status'] == "Не оплачено":
                print(f"   Задолженность: {car['debt']} руб.")
        else:
            print("   Статус: На стоянке")

        print("-" * 40)


# Функция просмотра должников
def show_debtors():
    print("\n=== Список должников ===")
    debtors = [car for car in cars_data if car["payment_status"] == "Не оплачено" and car["debt"] > 0]

    if not debtors:
        print("Должников нет.")
        return

    total_debt = sum(car["debt"] for car in debtors)
    print(f"Общая сумма задолженности: {total_debt} руб.")

    for i, car in enumerate(debtors, 1):
        print(f"{i}. Марка: {car['car_brand']}, Номер: {car['car_number']}")
        print(f"   Владелец: {car['owner_name']}")
        print(f"   Задолженность: {car['debt']} руб.")
        print("-" * 40)


# Главное меню
def main_menu():
    while True:
        print("\n=== АВТОСТОЯНКА ===")
        print("1. Добавить автомобиль на стоянку")
        print("2. Вывести автомобиль со стоянки")
        print("3. Показать текущие автомобили на стоянке")
        print("4. Просмотреть историю стоянки")
        print("5. Поиск автомобиля")
        print("6. Оплата задолженности")
        print("7. Просмотр должников")
        print("0. Выход")

        choice = input("\nВыберите действие: ")

        if choice == "1":
            add_car()
        elif choice == "2":
            remove_car()
        elif choice == "3":
            show_current_cars()
        elif choice == "4":
            show_history()
        elif choice == "5":
            search_car()
        elif choice == "6":
            pay_debt()
        elif choice == "7":
            show_debtors()
        elif choice == "0":
            print("Спасибо за использование программы!")
            break
        else:
            print("Неверный ввод. Попробуйте снова.")


if __name__ == "__main__":
    main_menu()
