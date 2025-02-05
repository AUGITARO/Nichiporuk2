from datetime import datetime, timedelta


def is_last_day_of_month(date):
    next_day = date + timedelta(days=1)
    return next_day.month != date.month


def get_holiday_greeting(date):
    holidays = {
        (1, 1): "Новым годом",
        (7, 1): "Рождеством",
        (23, 2): "Днём защитника Отечества",
        (8, 3): "Международным женским днём"
    }
    return holidays.get((date.day, date.month))


try:
    user_input = input("Введите дату в формате ДДММГГГГ: ").strip()

    if len(user_input) != 8 or not user_input.isdigit():
        raise ValueError("Некорректный формат даты")

    current_date = datetime.strptime(user_input, "%d%m%Y").date()

    messages = []

    # Проверка на последний день месяца
    if is_last_day_of_month(current_date):
        messages.append("Последний день месяца!")

    # Вычисление следующего дня
    next_day = current_date + timedelta(days=1)

    # Проверка на праздник
    holiday = get_holiday_greeting(next_day)
    if holiday:
        messages.append(f"С наступающим {holiday}!")

    # Форматирование следующей даты
    next_day_str = next_day.strftime("%d.%m.%Y")
    messages.append(f"Завтра {next_day_str}")

    print(" ".join(messages))

except ValueError as e:
    print(f"Ошибка: {e}")
