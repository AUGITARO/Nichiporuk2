# parking_app.py
import os
import json
import datetime
from datetime import datetime

data_file = "parking_data.json"
cars_data = []

if os.path.exists(data_file):
    with open(data_file, "r", encoding="utf-8") as file:
        cars_data = json.load(file)
else:
    cars_data = []


def save_data():
    with open(data_file, "w", encoding="utf-8") as file:
        json.dump(cars_data, file, ensure_ascii=False, indent=4, default=str)


def calculate_cost(entry_time, exit_time, hourly_rate, discount):
    time_diff = exit_time - entry_time
    hours = time_diff.total_seconds() / 3600
    cost = hours * hourly_rate
    discount_amount = cost * (discount / 100)
    final_cost = cost - discount_amount
    return max(0, round(final_cost, 2))


# Модифицированные функции для работы с параметрами
def add_car(brand, number, owner, discount):
    try:
        discount = int(discount)
        if discount < 0 or discount > 100:
            return "Ошибка: скидка должна быть от 0 до 100%"
    except ValueError:
        return "Ошибка: введите число для скидки"

    car = {
        "car_brand": brand,
        "car_number": number,
        "owner_name": owner,
        "entry_time": datetime.now(),
        "hourly_rate": 100,
        "discount": discount,
        "exit_time": None,
        "payment_status": "Не оплачено",
        "debt": 0.0
    }
    cars_data.append(car)
    save_data()
    return f"Автомобиль {brand} {number} добавлен"


def remove_car(car_number):
    for i, car in enumerate(cars_data):
        if car["car_number"] == car_number and car["exit_time"] is None:
            exit_time = datetime.now()
            entry_time = datetime.fromisoformat(str(car["entry_time"])) if isinstance(car["entry_time"], str) else car[
                "entry_time"]
            cost = calculate_cost(entry_time, exit_time, car["hourly_rate"], car["discount"])
            cars_data[i]["exit_time"] = exit_time
            cars_data[i]["debt"] = cost
            cars_data[i]["payment_status"] = "Не оплачено"
            save_data()
            return cost
    return None


def show_current_cars():
    return [car for car in cars_data if car["exit_time"] is None]


def show_history():
    return [car for car in cars_data if car["exit_time"] is not None]


def search_car(search_term):
    return [
        car for car in cars_data
        if (search_term.lower() in car["car_number"].lower() or
            search_term.lower() in car["car_brand"].lower() or
            search_term.lower() in car["owner_name"].lower())
    ]


def pay_debt(car_number):
    for i, car in enumerate(cars_data):
        if car["car_number"] == car_number and car["payment_status"] == "Не оплачено":
            cars_data[i]["payment_status"] = "Оплачено"
            cars_data[i]["debt"] = 0.0
            save_data()
            return True
    return False


def show_debtors():
    return [car for car in cars_data if car["payment_status"] == "Не оплачено" and car["debt"] > 0]