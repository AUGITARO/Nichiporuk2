# Программа 2: Сравнение методов оптимизации (оптимизированная версия с функциями)
# Реализация методов Фибоначчи, дихотомии и золотого сечения

import math


def input_data():
    """Получение входных данных от пользователя"""
    print("Программа для сравнения методов оптимизации")
    print("Введите данные для функции f(x) = a*x^2 + b*x + c")

    a = float(input("Введите коэффициент a: "))
    b = float(input("Введите коэффициент b: "))
    c = float(input("Введите коэффициент c: "))

    print("\nВведите границы интервала поиска и точность")
    left = float(input("Левая граница: "))
    right = float(input("Правая граница: "))
    eps = float(input("Точность (epsilon): "))

    return a, b, c, left, right, eps


def target_function(x, a, b, c):
    """Целевая функция f(x) = a*x^2 + b*x + c"""
    return a * x ** 2 + b * x + c


def dichotomy_method(f, left, right, eps, params):
    """
    Метод дихотомии для поиска минимума функции

    Args:
        f: целевая функция
        left, right: границы интервала
        eps: точность
        params: параметры для целевой функции

    Returns:
        tuple: (x_min, f_min, количество вычислений)
    """
    a, b = left, right
    delta = eps / 2  # Параметр для дихотомии
    count = 0

    while b - a > eps:
        x1 = (a + b - delta) / 2
        x2 = (a + b + delta) / 2

        f1 = f(x1, *params)
        f2 = f(x2, *params)
        count += 2  # Два вычисления функции

        if f1 <= f2:
            b = x2
        else:
            a = x1

    x_min = (a + b) / 2
    f_min = f(x_min, *params)
    count += 1  # Дополнительное вычисление для f_min

    return x_min, f_min, count


def golden_section_method(f, left, right, eps, params):
    """
    Метод золотого сечения для поиска минимума функции

    Args:
        f: целевая функция
        left, right: границы интервала
        eps: точность
        params: параметры для целевой функции

    Returns:
        tuple: (x_min, f_min, количество вычислений)
    """
    a, b = left, right
    golden_ratio = (math.sqrt(5) - 1) / 2  # ≈ 0.618
    count = 0

    x1 = a + (1 - golden_ratio) * (b - a)
    x2 = a + golden_ratio * (b - a)
    f1 = f(x1, *params)
    f2 = f(x2, *params)
    count += 2  # Два начальных вычисления функции

    while b - a > eps:
        if f1 <= f2:
            b = x2
            x2 = x1
            f2 = f1
            x1 = a + (1 - golden_ratio) * (b - a)
            f1 = f(x1, *params)
            count += 1
        else:
            a = x1
            x1 = x2
            f1 = f2
            x2 = a + golden_ratio * (b - a)
            f2 = f(x2, *params)
            count += 1

    x_min = (a + b) / 2
    f_min = f(x_min, *params)
    count += 1  # Дополнительное вычисление для f_min

    return x_min, f_min, count


def generate_fibonacci(n):
    """Генерирует последовательность чисел Фибоначчи до n-го числа"""
    fib = [1, 1]
    for i in range(2, n):
        fib.append(fib[i - 1] + fib[i - 2])
    return fib


def find_fibonacci_number(ratio, eps):
    """Находит подходящее число Фибоначчи для заданной точности"""
    fib = [1, 1]
    n = 2
    while fib[n - 1] <= ratio / eps:
        fib.append(fib[n - 1] + fib[n - 2])
        n += 1
    return fib, n - 1


def fibonacci_method(f, left, right, eps, params):
    """
    Метод Фибоначчи для поиска минимума функции

    Args:
        f: целевая функция
        left, right: границы интервала
        eps: точность
        params: параметры для целевой функции

    Returns:
        tuple: (x_min, f_min, количество вычислений, использованное число Фибоначчи)
    """
    a, b = left, right
    count = 0

    # Вычисление чисел Фибоначчи
    fib, n = find_fibonacci_number(b - a, eps)

    # Инициализация точек
    x1 = a + (fib[n - 2] / fib[n]) * (b - a)
    x2 = a + (fib[n - 1] / fib[n]) * (b - a)
    f1 = f(x1, *params)
    f2 = f(x2, *params)
    count += 2  # Два начальных вычисления функции

    # Итерации метода Фибоначчи
    k = 1
    while k < n - 2:
        if f1 > f2:
            a = x1
            x1 = x2
            f1 = f2
            x2 = a + (fib[n - k - 1] / fib[n - k]) * (b - a)
            f2 = f(x2, *params)
            count += 1
        else:
            b = x2
            x2 = x1
            f2 = f1
            x1 = a + (fib[n - k - 2] / fib[n - k]) * (b - a)
            f1 = f(x1, *params)
            count += 1
        k += 1

    # Последняя итерация
    if f1 > f2:
        a = x1
    else:
        b = x2

    x_min = (a + b) / 2
    f_min = f(x_min, *params)
    count += 1  # Дополнительное вычисление для f_min

    return x_min, f_min, count, fib[n]


def print_results(method_name, x_min, f_min, count, additional_info=None):
    """Вывод результатов метода"""
    print(f"\n{method_name}")
    if additional_info:
        print(additional_info)
    print(f"Результат: x_минимум = {x_min:.6f}, f(x_минимум) = {f_min:.6f}")
    print(f"Количество вычислений функции: {count}")
    return f"{x_min:.6f}", f"{f_min:.6f}", count


def main():
    """Основная функция программы"""
    # Получение входных данных
    a, b, c, left, right, eps = input_data()
    params = (a, b, c)  # Параметры для целевой функции

    # Применение метода дихотомии
    x_min_dichotomy, f_min_dichotomy, count_dichotomy = dichotomy_method(
        target_function, left, right, eps, params
    )
    dichotomy_results = print_results("1. Метод дихотомии", x_min_dichotomy, f_min_dichotomy, count_dichotomy)

    # Применение метода золотого сечения
    x_min_golden, f_min_golden, count_golden = golden_section_method(
        target_function, left, right, eps, params
    )
    golden_results = print_results("2. Метод золотого сечения", x_min_golden, f_min_golden, count_golden)

    # Применение метода Фибоначчи
    x_min_fibonacci, f_min_fibonacci, count_fibonacci, fib_number = fibonacci_method(
        target_function, left, right, eps, params
    )
    additional_info = f"Используемое число Фибоначчи: {fib_number}"
    fibonacci_results = print_results("3. Метод Фибоначчи", x_min_fibonacci, f_min_fibonacci, count_fibonacci,
                                      additional_info)

    # Итоговое сравнение
    print("\nИтоговое сравнение методов:")
    print(f"1. Дихотомия:       x = {x_min_dichotomy:.6f}, f(x) = {f_min_dichotomy:.6f}, вычислений: {count_dichotomy}")
    print(f"2. Золотое сечение: x = {x_min_golden:.6f}, f(x) = {f_min_golden:.6f}, вычислений: {count_golden}")
    print(f"3. Фибоначчи:       x = {x_min_fibonacci:.6f}, f(x) = {f_min_fibonacci:.6f}, вычислений: {count_fibonacci}")


if __name__ == "__main__":
    main()
