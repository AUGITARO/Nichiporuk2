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
