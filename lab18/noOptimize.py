import numpy as np
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D
from matplotlib import cm


def f(x, y):
    return (1 / (1 + ((x - 2) / 3) ** 2 + ((y - 2) / 3) ** 2)) + (3 / (1 + (x - 1) ** 2 + ((y - 1) / 2) ** 2))


def df_dx(x, y, h=0.0001):
    return (f(x + h, y) - f(x - h, y)) / (2 * h)


def df_dy(x, y, h=0.0001):
    return (f(x, y + h) - f(x, y - h)) / (2 * h)


def d2f_dx2(x, y, h=0.0001):
    return (f(x + h, y) - 2 * f(x, y) + f(x - h, y)) / (h ** 2)


def d2f_dy2(x, y, h=0.0001):
    return (f(x, y + h) - 2 * f(x, y) + f(x, y - h)) / (h ** 2)


def d2f_dxdy(x, y, h=0.0001):
    return (f(x + h, y + h) - f(x + h, y - h) - f(x - h, y + h) + f(x - h, y - h)) / (4 * h ** 2)


# Метод Гаусса (координатный спуск)
def gauss_method(start_x, start_y, alpha=0.1, max_iterations=1000, tolerance=1e-6):
    x = start_x
    y = start_y
    iteration = 0
    convergence_history = []

    while iteration < max_iterations:
        old_x = x
        old_y = y
        old_value = f(x, y)
        convergence_history.append((x, y, old_value))

        # Поиск по x
        x_step = alpha
        if f(x + x_step, y) < f(x, y):
            x_step = -alpha

        while f(x + x_step, y) > f(x, y):
            x = x + x_step

        # Поиск по y
        y_step = alpha
        if f(x, y + y_step) < f(x, y):
            y_step = -alpha

        while f(x, y + y_step) > f(x, y):
            y = y + y_step

        new_value = f(x, y)

        # Проверка сходимости
        if abs(new_value - old_value) < tolerance:
            break

        iteration += 1

    return x, y, f(x, y), convergence_history


# Метод Ньютона
def newton_method(start_x, start_y, max_iterations=100, tolerance=1e-6):
    x = start_x
    y = start_y
    iteration = 0
    convergence_history = []

    while iteration < max_iterations:
        old_value = f(x, y)
        convergence_history.append((x, y, old_value))

        # Вычисление градиента и матрицы Гессе
        gradient_x = df_dx(x, y)
        gradient_y = df_dy(x, y)

        hessian_xx = d2f_dx2(x, y)
        hessian_yy = d2f_dy2(x, y)
        hessian_xy = d2f_dxdy(x, y)

        # Определитель матрицы Гессе
        det_hessian = hessian_xx * hessian_yy - hessian_xy ** 2

        # Для поиска максимума матрица Гессе должна быть отрицательно определена
        if det_hessian == 0:
            # Если определитель равен нулю, используем небольшой шаг по градиенту
            x = x + 0.01 * gradient_x
            y = y + 0.01 * gradient_y
        else:
            # Обновляем координаты с использованием метода Ньютона
            delta_x = (hessian_yy * gradient_x - hessian_xy * gradient_y) / det_hessian
            delta_y = (hessian_xx * gradient_y - hessian_xy * gradient_x) / det_hessian

            # Для поиска максимума используем противоположное направление
            x = x + delta_x
            y = y + delta_y

        new_value = f(x, y)

        # Проверка сходимости
        if abs(new_value - old_value) < tolerance:
            break

        iteration += 1

    return x, y, f(x, y), convergence_history


# Визуализация функции
def plot_function_and_path(history, title):
    # Создаем сетку
    x = np.linspace(-1, 5, 100)
    y = np.linspace(-1, 5, 100)
    X, Y = np.meshgrid(x, y)
    Z = np.zeros_like(X)

    # Вычисляем значения функции
    for i in range(X.shape[0]):
        for j in range(X.shape[1]):
            Z[i, j] = f(X[i, j], Y[i, j])

    # Создаем 3D график
    fig = plt.figure(figsize=(12, 10))
    ax1 = fig.add_subplot(221, projection='3d')
    surf = ax1.plot_surface(X, Y, Z, cmap=cm.coolwarm, alpha=0.8)
    ax1.set_xlabel('X')
    ax1.set_ylabel('Y')
    ax1.set_zlabel('f(X, Y)')
    ax1.set_title(f'3D поверхность функции с траекторией ({title})')

    # Добавляем путь оптимизации на 3D графике
    path_x = [p[0] for p in history]
    path_y = [p[1] for p in history]
    path_z = [p[2] for p in history]
    ax1.plot(path_x, path_y, path_z, 'r-o', lw=2, markersize=3)

    # Создаем 2D график с контурами
    ax2 = fig.add_subplot(222)
    contour = ax2.contourf(X, Y, Z, levels=50, cmap=cm.coolwarm)
    fig.colorbar(contour, ax=ax2)
    ax2.set_xlabel('X')
    ax2.set_ylabel('Y')
    ax2.set_title(f'Контурный график с траекторией ({title})')

    # Добавляем путь оптимизации на контурном графике
    ax2.plot(path_x, path_y, 'r-o', lw=2, markersize=3)

    # График сходимости
    ax3 = fig.add_subplot(212)
    ax3.plot(range(len(path_z)), path_z, 'b-', lw=2)
    ax3.set_xlabel('Итерация')
    ax3.set_ylabel('f(X, Y)')
    ax3.set_title(f'График сходимости ({title})')
    ax3.grid(True)

    plt.tight_layout()
    return fig


# Основной блок
def main():
    # Начальная точка
    start_x = 0.0
    start_y = 0.0

    # Запуск метода Гаусса
    gauss_x, gauss_y, gauss_value, gauss_history = gauss_method(start_x, start_y)
    print("\nРезультаты метода Гаусса:")
    print(f"Точка максимума: x = {gauss_x:.6f}, y = {gauss_y:.6f}")
    print(f"Значение функции: f(x,y) = {gauss_value:.6f}")
    print(f"Количество итераций: {len(gauss_history)}")

    # Визуализация для метода Гаусса
    gauss_fig = plot_function_and_path(gauss_history, "Метод Гаусса")

    # Запуск метода Ньютона
    newton_x, newton_y, newton_value, newton_history = newton_method(start_x, start_y)
    print("\nРезультаты метода Ньютона:")
    print(f"Точка максимума: x = {newton_x:.6f}, y = {newton_y:.6f}")
    print(f"Значение функции: f(x,y) = {newton_value:.6f}")
    print(f"Количество итераций: {len(newton_history)}")

    # Визуализация для метода Ньютона
    newton_fig = plot_function_and_path(newton_history, "Метод Ньютона")

    plt.show()


if __name__ == "__main__":
    main()