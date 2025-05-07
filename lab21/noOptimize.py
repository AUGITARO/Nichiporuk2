import numpy as np

# Квадратичная функция
def f1(x1, x2):
    return 100*(x2 - x1)**2 + (1 - x1)**2

# Функция Розенброка
def f2(x1, x2):
    return 100*(x2 - x1**2)**2 + (1 - x1)**2

# Тестовая функция варианта
def f3(x, y):
    return (1/(1 + ((x-2)/3)**2 + ((y-2)/3)**2) +
           3/(1 + (x-1)**2 + ((y-1)/2)**2))

# Градиентный спуск (упрощенная реализация)
def gradient_descent(func, start_x, start_y, lr=0.001, max_iter=1000):
    x, y = start_x, start_y
    for _ in range(max_iter):
        grad_x = (func(x + 0.001, y) - func(x - 0.001, y)) / 0.002
        grad_y = (func(x, y + 0.001) - func(x, y - 0.001)) / 0.002
        x -= lr * grad_x
        y -= lr * grad_y
    return x, y, func(x, y)

# Исследование для f1
points = [(0,0), (2,2)]
for point in points:
    result = gradient_descent(f1, *point)
    print(f"f1: Начало {point} -> Минимум ({result[0]:.4f}, {result[1]:.4f}), значение={result[2]:.4f}")

# Исследование для f2
for point in points:
    result = gradient_descent(f2, *point)
    print(f"f2: Начало {point} -> Минимум ({result[0]:.4f}, {result[1]:.4f}), значение={result[2]:.4f}")

# Исследование для f3
points = [(0,0), (3,3)]
for point in points:
    result = gradient_descent(f3, *point)
    print(f"f3: Начало {point} -> Минимум ({result[0]:.4f}, {result[1]:.4f}), значение={result[2]:.4f}")
