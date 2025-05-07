import numpy as np
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D


def objective_function(x, y):
    """Целевая функция f(x, y) = 10*(y - x)^2 + y^2"""
    return 10 * (y - x) ** 2 + y ** 2


def constraint(x, y):
    """
    Функция ограничения преобразованная так, чтобы g(x,y) > 0
    Ограничение x = 2 - y преобразуем в g(x,y) = (2 - y) - x
    Тогда g(x,y) > 0 означает x < 2 - y
    """
    return (2 - y) - x


def barrier_function(x, y, mu):
    """
    Барьерная функция, добавляющая штраф при приближении к границе допустимой области
    Принимает:
        x, y - координаты точки
        mu - параметр барьера
    Возвращает:
        Значение барьерной функции или бесконечность, если точка недопустима
    """
    constr_val = constraint(x, y)
    if constr_val <= 0:
        return float('inf')  # За пределами допустимой области возвращаем бесконечность
    return objective_function(x, y) - mu * np.log(constr_val)


def find_feasible_point():
    """Находит начальную точку в допустимой области"""
    for test_x in np.linspace(-1, 1, 20):
        for test_y in np.linspace(-1, 1, 20):
            if constraint(test_x, test_y) > 0:
                return test_x, test_y
    # Если не удалось найти точку, возвращаем безопасное значение
    return 0.0, 1.0  # Точка (0,1) явно удовлетворяет ограничению x < 2 - y


def coordinate_descent_step(x, y, mu, alpha):
    """
    Выполняет один шаг метода координатного спуска для барьерной функции
    Принимает:
        x, y - текущая точка
        mu - параметр барьера
        alpha - шаг для координатного спуска
    Возвращает:
        Новые значения x, y
    """
    # Текущее значение барьерной функции
    current_value = barrier_function(x, y, mu)

    # Расчет направления поиска по x
    x_plus = x + alpha
    x_minus = x - alpha

    value_plus_x = barrier_function(x_plus, y, mu)
    value_minus_x = barrier_function(x_minus, y, mu)

    # Выбираем лучшее направление по x
    if value_plus_x < current_value and value_plus_x < value_minus_x:
        x = x_plus
    elif value_minus_x < current_value:
        x = x_minus

    # Обновляем текущее значение после шага по x
    current_value = barrier_function(x, y, mu)

    # Расчет направления поиска по y
    y_plus = y + alpha
    y_minus = y - alpha

    value_plus_y = barrier_function(x, y_plus, mu)
    value_minus_y = barrier_function(x, y_minus, mu)

    # Выбираем лучшее направление по y
    if value_plus_y < current_value and value_plus_y < value_minus_y:
        y = y_plus
    elif value_minus_y < current_value:
        y = y_minus

    return x, y


def check_inner_convergence(x, y, mu, prev_value, epsilon):
    """
    Проверяет сходимость внутреннего цикла
    Принимает:
        x, y - текущая точка
        mu - параметр барьера
        prev_value - предыдущее значение функции
        epsilon - точность
    Возвращает:
        True, если достигнута сходимость, иначе False
    """
    new_value = barrier_function(x, y, mu)
    return abs(prev_value - new_value) < epsilon


def optimize(x0=None, y0=None, mu0=1.0, alpha=0.01, epsilon=1e-6, mu_reduction_factor=0.1,
             max_iterations=1000, max_inner_iterations=100):
    """
    Основная функция оптимизации с методом барьерных функций и координатным спуском

    Параметры:
    x0, y0 - начальная точка (если None, то будет найдена допустимая точка)
    mu0 - начальный параметр барьера
    alpha - шаг для координатного спуска
    epsilon - точность
    mu_reduction_factor - множитель для уменьшения параметра барьера
    max_iterations - максимальное число внешних итераций
    max_inner_iterations - максимальное число внутренних итераций

    Возвращает:
    x, y - найденная точка минимума
    history - история точек для визуализации
    iterations - число итераций
    """
    # Если начальная точка не задана или находится вне допустимой области, находим подходящую
    if x0 is None or y0 is None or constraint(x0, y0) <= 0:
        x, y = find_feasible_point()
    else:
        x, y = x0, y0

    mu = mu0

    # История для визуализации
    history = {'x': [x], 'y': [y], 'f': [objective_function(x, y)]}

    # Внешний цикл - уменьшение параметра барьера
    iteration = 0
    converged = False

    while not converged and iteration < max_iterations:
        # Внутренний цикл - поиск минимума текущей барьерной функции
        inner_iteration = 0
        inner_converged = False
        prev_value = barrier_function(x, y, mu)

        while not inner_converged and inner_iteration < max_inner_iterations:
            # Шаг оптимизации
            x, y = coordinate_descent_step(x, y, mu, alpha)

            # Записываем историю
            history['x'].append(x)
            history['y'].append(y)
            history['f'].append(objective_function(x, y))

            # Проверяем условие сходимости внутреннего цикла
            inner_converged = check_inner_convergence(x, y, mu, prev_value, epsilon)
            prev_value = barrier_function(x, y, mu)

            inner_iteration += 1

        # Проверка условия сходимости внешнего цикла
        if mu < epsilon:
            converged = True
        else:
            # Уменьшаем параметр барьера
            mu *= mu_reduction_factor

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

    # Заштриховываем недопустимую область (x > 2 - y)
    invalid_x = np.linspace(-1, 3, 100)
    invalid_y = np.linspace(-1, 3, 100)
    invalid_X, invalid_Y = np.meshgrid(invalid_x, invalid_y)
    invalid_mask = invalid_X > (2 - invalid_Y)
    ax2.contourf(invalid_X, invalid_Y, invalid_mask.astype(float), levels=[0.5, 1.5], colors='gray', alpha=0.3)

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
    mu0 = 1.0  # начальный параметр барьера
    alpha = 0.01  # шаг для координатного спуска
    epsilon = 1e-6  # точность
    mu_reduction_factor = 0.1  # множитель для уменьшения параметра барьера

    # Запуск оптимизации (начальная точка будет найдена автоматически)
    x_opt, y_opt, history, iterations = optimize(
        mu0=mu0, alpha=alpha, epsilon=epsilon,
        mu_reduction_factor=mu_reduction_factor
    )

    # Вывод результатов
    print(f"Найденная точка минимума: x = {x_opt:.6f}, y = {y_opt:.6f}")
    print(f"Значение функции: f(x,y) = {objective_function(x_opt, y_opt):.6f}")
    print(f"Значение ограничения: g(x,y) = {constraint(x_opt, y_opt):.6f}")
    print(f"Количество итераций: {iterations}")

    # Визуализация
    visualize_results(x_opt, y_opt, history)


if __name__ == "__main__":
    main()
