import numpy as np
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D


def objective_function(x, y):
    """Целевая функция f(x, y) = 10*(y - x)^2 + y^2"""
    return 10 * (y - x) ** 2 + y ** 2


def constraint(x, y):
    """Ограничение x = 2 - y, преобразованное в g(x, y) = x - (2 - y)"""
    return x - (2 - y)


def penalty_function(x, y, r):
    """Штрафная функция F(x,y) = f(x,y) + r*g(x,y)^2"""
    return objective_function(x, y) + r * constraint(x, y) ** 2


def coordinate_descent_step(x, y, r, alpha):
    """Выполняет один шаг метода координатного спуска"""
    # Шаг по x
    if penalty_function(x + alpha, y, r) < penalty_function(x, y, r):
        x = x + alpha
    elif penalty_function(x - alpha, y, r) < penalty_function(x, y, r):
        x = x - alpha

    # Шаг по y
    if penalty_function(x, y + alpha, r) < penalty_function(x, y, r):
        y = y + alpha
    elif penalty_function(x, y - alpha, r) < penalty_function(x, y, r):
        y = y - alpha

    return x, y


def check_inner_convergence(x, y, r, alpha, epsilon):
    """Проверяет сходимость внутреннего цикла"""
    current_value = penalty_function(x, y, r)
    next_x = x + alpha if penalty_function(x + alpha, y, r) < penalty_function(x - alpha, y, r) else x - alpha
    next_y = y + alpha if penalty_function(x, y + alpha, r) < penalty_function(x, y - alpha, r) else y - alpha
    next_value = penalty_function(next_x, next_y, r)

    return abs(current_value - next_value) < epsilon


def optimize(x0=0.0, y0=0.0, r0=1.0, alpha=0.01, epsilon=1e-6, beta=10.0,
             max_iterations=10000, max_inner_iterations=100):
    """
    Основная функция оптимизации с методом штрафных функций и координатным спуском

    Параметры:
    x0, y0 - начальная точка
    r0 - начальный коэффициент штрафа
    alpha - шаг для координатного спуска
    epsilon - точность
    beta - множитель для увеличения штрафа
    max_iterations - максимальное число внешних итераций
    max_inner_iterations - максимальное число внутренних итераций

    Возвращает:
    x, y - найденная точка минимума
    history - история точек для визуализации
    iterations - число итераций
    """
    x, y = x0, y0
    r = r0

    # История для визуализации
    history = {'x': [x], 'y': [y], 'f': [objective_function(x, y)]}

    # Внешний цикл - увеличение штрафа
    iteration = 0
    converged = False

    while not converged and iteration < max_iterations:
        # Внутренний цикл - поиск минимума текущей штрафной функции
        inner_iteration = 0
        inner_converged = False

        while not inner_converged and inner_iteration < max_inner_iterations:
            # Шаг оптимизации
            x, y = coordinate_descent_step(x, y, r, alpha)

            # Записываем историю
            history['x'].append(x)
            history['y'].append(y)
            history['f'].append(objective_function(x, y))

            # Проверяем условие сходимости внутреннего цикла
            inner_converged = check_inner_convergence(x, y, r, alpha, epsilon)
            inner_iteration += 1

        # Проверка сходимости по ограничению
        if abs(constraint(x, y)) < epsilon:
            converged = True
        else:
            # Увеличиваем коэффициент штрафа
            r *= beta

        iteration += 1

    return x, y, history, iteration


def visualize_results(x_opt, y_opt, history):
    """Визуализирует результаты оптимизации"""
    # Создаем сетку для графика
    x_range = np.linspace(-1, 3, 100)
    y_range = np.linspace(-1, 3, 100)
    X, Y = np.meshgrid(x_range, y_range)
    Z = np.zeros_like(X)

    for i in range(len(x_range)):
        for j in range(len(y_range)):
            Z[j, i] = objective_function(X[i, j], Y[j, i])

    # Создаем 3D график
    fig = plt.figure(figsize=(14, 6))

    # 3D поверхность функции
    ax1 = fig.add_subplot(121, projection='3d')
    surf = ax1.plot_surface(X, Y, Z, cmap='viridis', alpha=0.8)
    ax1.set_xlabel('X')
    ax1.set_ylabel('Y')
    ax1.set_zlabel('f(X,Y)')
    ax1.set_title('Целевая функция')

    # Отображаем точки оптимизации на поверхности
    path_z = [objective_function(x, y) for x, y in zip(history['x'], history['y'])]
    ax1.scatter(history['x'], history['y'], path_z, color='r', s=10, alpha=0.6)

    # 2D контурный график с ограничением
    ax2 = fig.add_subplot(122)
    contour = ax2.contour(X, Y, Z, 50, cmap='viridis')
    ax2.set_xlabel('X')
    ax2.set_ylabel('Y')
    ax2.set_title('Контурный график с ограничением')

    # Отображаем ограничение x = 2 - y
    constraint_x = np.linspace(-1, 3, 100)
    constraint_y = 2 - constraint_x
    ax2.plot(constraint_x, constraint_y, 'r--', label='x = 2 - y')

    # Отображаем путь оптимизации
    ax2.plot(history['x'], history['y'], 'b-', alpha=0.6)
    ax2.scatter(history['x'], history['y'], color='b', s=10, alpha=0.6)
    ax2.scatter(x_opt, y_opt, color='r', s=100, marker='*', label='Минимум')

    ax2.legend()
    plt.colorbar(contour, ax=ax2)
    plt.tight_layout()
    plt.show()


def main():
    # Параметры оптимизации
    x0, y0 = 0.0, 0.0  # начальная точка
    r0 = 1.0  # начальный коэффициент штрафа
    alpha = 0.01  # шаг для координатного спуска
    epsilon = 1e-6  # точность
    beta = 10.0  # множитель для увеличения штрафа

    # Запуск оптимизации
    x_opt, y_opt, history, iterations = optimize(x0, y0, r0, alpha, epsilon, beta)

    # Вывод результатов
    print(f"Найденная точка минимума: x = {x_opt:.6f}, y = {y_opt:.6f}")
    print(f"Значение функции: f(x,y) = {objective_function(x_opt, y_opt):.6f}")
    print(f"Значение ограничения: g(x,y) = {constraint(x_opt, y_opt):.6f}")
    print(f"Количество итераций: {iterations}")

    # Визуализация
    visualize_results(x_opt, y_opt, history)


if __name__ == "__main__":
    main()
