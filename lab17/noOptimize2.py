import numpy as np
import matplotlib.pyplot as plt

# Параметры задачи
left_border = -2.0
right_border = 20.0
n_points_list = [5, 10, 20, 50, 100]

# Создание фигуры для графиков
plt.figure(figsize=(15, 10))

# Вывод результатов
print("Результаты поиска интервала с минимумом функции f(x) = (x-8)^2")
print("Метод: Пассивный поиск (базовые конструкции)")

# Цикл по количеству точек
for i, n_points in enumerate(n_points_list, 1):
    # Инициализация переменных для хранения результатов
    min_x = 0
    min_value = float('inf')

    # Создание массивов для хранения точек
    x_points = np.linspace(left_border, right_border, n_points)
    y_points = (x_points - 8) ** 2

    # Поиск минимума
    min_index = np.argmin(y_points)
    min_x = x_points[min_index]
    min_value = y_points[min_index]

    # Вывод результатов для текущего количества точек
    print(f"\nКоличество точек: {n_points}")
    print(f"Координата минимума: {min_x:.4f}")
    print(f"Значение минимума: {min_value:.4f}")

    # Создание subplot
    plt.subplot(2, 3, i)

    # Создание более гладкой кривой для отрисовки
    x_smooth = np.linspace(left_border, right_border, 200)
    y_smooth = (x_smooth - 8) ** 2

    # Построение графика функции
    plt.plot(x_smooth, y_smooth, 'b-', label='f(x) = (x-8)²')

    # Точки выборки
    plt.scatter(x_points, y_points, color='red', label='Выборка')

    # Точка минимума
    plt.scatter(min_x, min_value, color='green', s=100, label='Минимум')

    plt.title(f'Поиск минимума\n({n_points} точек)')
    plt.xlabel('x')
    plt.ylabel('f(x)')
    plt.legend()
    plt.grid(True)

# Корректировка расположения субплотов
plt.tight_layout()

# Отображение графиков
plt.show()