import numpy as np
import matplotlib.pyplot as plt
from typing import Tuple, List


def target_function(x: float) -> float:
    """
    Целевая функция для поиска минимума.
    f(x) = (x-8)^2
    """
    return (x - 8) ** 2


def find_minimum_in_interval(
        left_border: float,
        right_border: float,
        n_points: int
) -> Tuple[float, float]:
    """
    Находит минимум функции в заданном интервале с использованием дискретной выборки.

    Args:
        left_border (float): Левая граница интервала
        right_border (float): Правая граница интервала
        n_points (int): Количество точек для выборки

    Returns:
        Tuple[float, float]: Координата и значение минимума
    """
    # Создание массивов для хранения точек
    x_points = np.linspace(left_border, right_border, n_points)
    y_points = target_function(x_points)

    # Поиск минимума
    min_index = np.argmin(y_points)
    return x_points[min_index], y_points[min_index]


def plot_function_search(
        left_border: float,
        right_border: float,
        n_points: int,
        subplot_pos: int
):
    """
    Визуализация поиска минимума функции.

    Args:
        left_border (float): Левая граница интервала
        right_border (float): Правая граница интервала
        n_points (int): Количество точек для выборки
        subplot_pos (int): Позиция subplot
    """
    # Поиск минимума
    min_x, min_value = find_minimum_in_interval(left_border, right_border, n_points)

    # Вывод результатов для текущего количества точек
    print(f"\nКоличество точек: {n_points}")
    print(f"Координата минимума: {min_x:.4f}")
    print(f"Значение минимума: {min_value:.4f}")

    # Создание subplot
    plt.subplot(2, 3, subplot_pos)

    # Создание более гладкой кривой для отрисовки
    x_smooth = np.linspace(left_border, right_border, 200)
    y_smooth = target_function(x_smooth)

    # Создание массивов для хранения точек
    x_points = np.linspace(left_border, right_border, n_points)
    y_points = target_function(x_points)

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


def main():
    """
    Основная функция для выполнения поиска минимума и визуализации.
    """
    # Параметры задачи
    left_border = -2.0
    right_border = 20.0
    n_points_list = [5, 10, 20, 50, 100]

    # Создание фигуры для графиков
    plt.figure(figsize=(15, 10))

    # Вывод результатов
    print("Результаты поиска интервала с минимумом функции f(x) = (x-8)^2")
    print("Метод: Пассивный поиск (с использованием функций)")

    # Визуализация для каждого количества точек
    for i, n_points in enumerate(n_points_list, 1):
        plot_function_search(left_border, right_border, n_points, i)

    # Корректировка расположения субплотов
    plt.tight_layout()

    # Отображение графиков
    plt.show()


# Точка входа в программу
if __name__ == "__main__":
    main()