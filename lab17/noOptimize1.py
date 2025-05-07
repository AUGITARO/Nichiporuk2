import matplotlib.pyplot as plt
import math

epsilons = [10**(-i) for i in range(1, 8)]

# Метод дихотомии
dichotomy_counts = []
for eps in epsilons:
    a, b, count = -2.0, 20.0, 0
    while b - a > eps:
        c = (a + b) / 2
        delta = (b - a) * 0.25
        x1, x2 = c - delta, c + delta
        f1, f2 = (x1-7)**2, (x2-7)**2
        count += 2
        if f1 < f2:
            b = x2
        else:
            a = x1
    dichotomy_counts.append(count)

# Метод золотого сечения
golden_counts = []
phi = (math.sqrt(5) - 1) / 2
for eps in epsilons:
    a, b, count = -2.0, 20.0, 2
    x1 = a + (1 - phi)*(b - a)
    x2 = a + phi*(b - a)
    f1, f2 = (x1-7)**2, (x2-7)**2
    while b - a > eps:
        if f1 < f2:
            b, x2, f2 = x2, x1, f1
            x1 = a + (1 - phi)*(b - a)
            f1 = (x1-7)**2
        else:
            a, x1, f1 = x1, x2, f2
            x2 = a + phi*(b - a)
            f2 = (x2-7)**2
        count += 1
    golden_counts.append(count)

# Построение графика
log_eps = [math.log10(eps) for eps in epsilons]
plt.plot(log_eps, dichotomy_counts, marker='o', label='Дихотомия')
plt.plot(log_eps, golden_counts, marker='s', label='Золотое сечение')
plt.xlabel('log10(эпсилон)')
plt.ylabel('Количество вычислений функции')
plt.legend()
plt.grid(True)
plt.show()