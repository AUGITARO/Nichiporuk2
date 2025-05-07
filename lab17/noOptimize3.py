# Программа 1: Сравнение методов оптимизации (элементарные конструкции)
# Реализация методов Фибоначчи, дихотомии и золотого сечения

import math

print("Программа для сравнения методов оптимизации")

# Функция, которую мы минимизируем
print("Введите данные для функции f(x) = a*x^2 + b*x + c")
a = float(input("Введите коэффициент a: "))
b = float(input("Введите коэффициент b: "))
c = float(input("Введите коэффициент c: "))

# Входные параметры для всех методов
print("\nВведите границы интервала поиска и точность")
left = float(input("Левая граница: "))
right = float(input("Правая граница: "))
eps = float(input("Точность (epsilon): "))

# Счетчики вычислений функции для каждого метода
count_dichotomy = 0
count_golden_section = 0
count_fibonacci = 0


# Вычисление значения функции
def f(x):
    return a * x ** 2 + b * x + c


print("\n1. Метод дихотомии")
# Метод дихотомии
a_dichot = left
b_dichot = right
delta = eps / 2  # Параметр для дихотомии

while b_dichot - a_dichot > eps:
    x1 = (a_dichot + b_dichot - delta) / 2
    x2 = (a_dichot + b_dichot + delta) / 2

    f1 = f(x1)
    f2 = f(x2)
    count_dichotomy += 2  # Два вычисления функции

    if f1 <= f2:
        b_dichot = x2
    else:
        a_dichot = x1

x_min_dichotomy = (a_dichot + b_dichot) / 2
f_min_dichotomy = f(x_min_dichotomy)
count_dichotomy += 1  # Дополнительное вычисление для f_min

print(f"Результат: x_минимум = {x_min_dichotomy:.6f}, f(x_минимум) = {f_min_dichotomy:.6f}")
print(f"Количество вычислений функции: {count_dichotomy}")

print("\n2. Метод золотого сечения")
# Метод золотого сечения
a_golden = left
b_golden = right
golden_ratio = (math.sqrt(5) - 1) / 2  # ≈ 0.618

x1 = a_golden + (1 - golden_ratio) * (b_golden - a_golden)
x2 = a_golden + golden_ratio * (b_golden - a_golden)
f1 = f(x1)
f2 = f(x2)
count_golden_section += 2  # Два начальных вычисления функции

while b_golden - a_golden > eps:
    if f1 <= f2:
        b_golden = x2
        x2 = x1
        f2 = f1
        x1 = a_golden + (1 - golden_ratio) * (b_golden - a_golden)
        f1 = f(x1)
        count_golden_section += 1
    else:
        a_golden = x1
        x1 = x2
        f1 = f2
        x2 = a_golden + golden_ratio * (b_golden - a_golden)
        f2 = f(x2)
        count_golden_section += 1

x_min_golden = (a_golden + b_golden) / 2
f_min_golden = f(x_min_golden)
count_golden_section += 1  # Дополнительное вычисление для f_min

print(f"Результат: x_минимум = {x_min_golden:.6f}, f(x_минимум) = {f_min_golden:.6f}")
print(f"Количество вычислений функции: {count_golden_section}")

print("\n3. Метод Фибоначчи")
# Метод Фибоначчи
a_fib = left
b_fib = right

# Вычисление чисел Фибоначчи
fib = [1, 1]  # Первые два числа Фибоначчи
n = 2  # Уже вычислены 2 числа
while fib[n - 1] <= (b_fib - a_fib) / eps:
    fib.append(fib[n - 1] + fib[n - 2])
    n += 1

n = n - 1  # Индекс последнего вычисленного числа
print(f"Используемое число Фибоначчи: {fib[n]}")

# Инициализация точек
x1 = a_fib + (fib[n - 2] / fib[n]) * (b_fib - a_fib)
x2 = a_fib + (fib[n - 1] / fib[n]) * (b_fib - a_fib)
f1 = f(x1)
f2 = f(x2)
count_fibonacci += 2  # Два начальных вычисления функции

# Итерации метода Фибоначчи
k = 1
while k < n - 2:
    if f1 > f2:
        a_fib = x1
        x1 = x2
        f1 = f2
        x2 = a_fib + (fib[n - k - 1] / fib[n - k]) * (b_fib - a_fib)
        f2 = f(x2)
        count_fibonacci += 1
    else:
        b_fib = x2
        x2 = x1
        f2 = f1
        x1 = a_fib + (fib[n - k - 2] / fib[n - k]) * (b_fib - a_fib)
        f1 = f(x1)
        count_fibonacci += 1
    k += 1

# Последняя итерация
if f1 > f2:
    a_fib = x1
else:
    b_fib = x2

x_min_fibonacci = (a_fib + b_fib) / 2
f_min_fibonacci = f(x_min_fibonacci)
count_fibonacci += 1  # Дополнительное вычисление для f_min

print(f"Результат: x_минимум = {x_min_fibonacci:.6f}, f(x_минимум) = {f_min_fibonacci:.6f}")
print(f"Количество вычислений функции: {count_fibonacci}")

print("\nИтоговое сравнение методов:")
print(f"1. Дихотомия:       x = {x_min_dichotomy:.6f}, f(x) = {f_min_dichotomy:.6f}, вычислений: {count_dichotomy}")
print(f"2. Золотое сечение: x = {x_min_golden:.6f}, f(x) = {f_min_golden:.6f}, вычислений: {count_golden_section}")
print(f"3. Фибоначчи:       x = {x_min_fibonacci:.6f}, f(x) = {f_min_fibonacci:.6f}, вычислений: {count_fibonacci}")
