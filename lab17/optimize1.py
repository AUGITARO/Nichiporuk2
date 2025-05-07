import matplotlib.pyplot as plt
import math

def dichotomy_method(a_init, b_init, epsilon):
    """Метод дихотомии для поиска минимума функции"""
    a, b, count = a_init, b_init, 0
    while b - a > epsilon:
        c = (a + b) / 2
        delta = (b - a) * 0.25
        x1, x2 = c - delta, c + delta
        f1, f2 = (x1-7)**2, (x2-7)**2
        count += 2
        if f1 < f2:
            b = x2
        else:
            a = x1
    return count

def golden_section_method(a_init, b_init, epsilon):
    """Метод золотого сечения для поиска минимума функции"""
    phi = (math.sqrt(5) - 1) / 2
    a, b, count = a_init, b_init, 2
    x1 = a + (1 - phi)*(b - a)
    x2 = a + phi*(b - a)
    f1, f2 = (x1-7)**2, (x2-7)**2
    while b - a > epsilon:
        if f1 < f2:
            b, x2, f2 = x2, x1, f1
            x1 = a + (1 - phi)*(b - a)
            f1 = (x1-7)**2
        else:
            a, x1, f1 = x1, x2, f2
            x2 = a + phi*(b - a)
            f2 = (x2-7)**2
        count += 1
    return count

epsilons = [10**(-i) for i in range(1, 8)]
dichotomy_counts = [dichotomy_method(-2, 20, eps) for eps in epsilons]
golden_counts = [golden_section_method(-2, 20, eps) for eps in epsilons]

log_eps = [math.log10(eps) for eps in epsilons]
plt.plot(log_eps, dichotomy_counts, marker='o', label='Дихотомия')
plt.plot(log_eps, golden_counts, marker='s', label='Золотое сечение')
plt.xlabel('log10(эпсилон)')
plt.ylabel('Число вычислений функции')
plt.legend()
plt.grid(True)
plt.show()
