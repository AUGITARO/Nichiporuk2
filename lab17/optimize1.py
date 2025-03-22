import matplotlib.pyplot as plt
import math

# Целевая функция
def f1(x):
    return (x - 7) ** 2

# Метод дихотомии
def dichotomy(f, a, b, epsilon):
    calls = 0
    delta = epsilon / 2
    while (b - a) > 2 * epsilon:
        mid = (a + b) / 2
        x1 = mid - delta
        x2 = mid + delta
        if f(x1) < f(x2):
            b = x2
        else:
            a = x1
        calls += 2
    return (a + b) / 2, calls


# Метод золотого сечения
def golden_section(f, a, b, epsilon):
    calls = 0
    phi = (math.sqrt(5) - 1) / 2
    x1 = a + (1 - phi) * (b - a)
    x2 = a + phi * (b - a)
    f1_val = f(x1)
    f2_val = f(x2)
    calls += 2

    while (b - a) > 2 * epsilon:
        if f1_val < f2_val:
            b = x2
            x2 = x1
            f2_val = f1_val
            x1 = a + (1 - phi) * (b - a)
            f1_val = f(x1)
            calls += 1
        else:
            a = x1
            x1 = x2
            f1_val = f2_val
            x2 = a + phi * (b - a)
            f2_val = f(x2)
            calls += 1
    return (a + b) / 2, calls


# Исследование сходимости и построение графика
epsilons = [10 ** -i for i in range(1, 8)]
dichotomy_counts = []
golden_counts = []

for eps in epsilons:
    _, dc = dichotomy(f1, -2, 20, eps)
    _, gc = golden_section(f1, -2, 20, eps)
    dichotomy_counts.append(dc)
    golden_counts.append(gc)

plt.figure(figsize=(10, 6))
plt.plot([math.log10(eps) for eps in epsilons], dichotomy_counts, label='Метод дихотомии')
plt.plot([math.log10(eps) for eps in epsilons], golden_counts, label='Метод золотого сечения')
plt.xlabel('log10(epsilon)')
plt.ylabel('Функции')
plt.legend()
plt.grid(True)
plt.show()