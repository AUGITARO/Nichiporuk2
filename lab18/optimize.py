import numpy as np
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D
from matplotlib import cm
import time


class FunctionOptimizer:
    def __init__(self, func, start_x=0.0, start_y=0.0, tolerance=1e-6):
        """
        Инициализация оптимизатора функции.

        Parameters:
        - func: оптимизируемая функция двух переменных
        - start_x, start_y: начальные координаты
        - tolerance: критерий остановки оптимизации
        """
        self.func = func
        self.start_x = start_x
        self.start_y = start_y
        self.tolerance = tolerance

    def _compute_gradient(self, x, y, h=0.0001):
        """Вычисление градиента функции"""
        df_dx = (self.func(x + h, y) - self.func(x - h, y)) / (2 * h)
        df_dy = (self.func(x, y + h) - self.func(x, y - h)) / (2 * h)
        return df_dx, df_dy

    def _compute_hessian(self, x, y, h=0.0001):
        """Вычисление матрицы Гессе"""
        d2f_dx2 = (self.func(x + h, y) - 2 * self.func(x, y) + self.func(x - h, y)) / (h ** 2)
        d2f_dy2 = (self.func(x, y + h) - 2 * self.func(x, y) + self.func(x, y - h)) / (h ** 2)
        d2f_dxdy = (self.func(x + h, y + h) - self.func(x + h, y - h) -
                    self.func(x - h, y + h) + self.func(x - h, y - h)) / (4 * h ** 2)

        return d2f_dx2, d2f_dy2, d2f_dxdy

    def gauss_method(self, alpha=0.1, max_iterations=1000):
        """
        Метод Гаусса (координатный спуск) для поиска максимума функции.

        Parameters:
        - alpha: начальный шаг
        - max_iterations: максимальное число итераций

        Returns:
        - x, y: найденные координаты максимума
        - value: значение функции в точке максимума
        - history: история оптимизации
        - time_elapsed: время выполнения алгоритма
        """
        start_time = time.time()
        x, y = self.start_x, self.start_y
        iteration = 0
        history = []

        while iteration < max_iterations:
            old_value = self.func(x, y)
            history.append((x, y, old_value))

            # Поиск по x
            x_step = alpha
            if self.func(x + x_step, y) < self.func(x, y):
                x_step = -alpha

            # Линейный поиск по x
            while self.func(x + x_step, y) > self.func(x, y):
                x = x + x_step

            # Поиск по y
            y_step = alpha
            if self.func(x, y + y_step) < self.func(x, y):
                y_step = -alpha

            # Линейный поиск по y
            while self.func(x, y + y_step) > self.func(x, y):
                y = y + y_step

            new_value = self.func(x, y)

            # Проверка сходимости
            if abs(new_value - old_value) < self.tolerance:
                break

            iteration += 1

        time_elapsed = time.time() - start_time
        return x, y, self.func(x, y), history, time_elapsed

    def newton_method(self, max_iterations=100):
        """
        Метод Ньютона для поиска максимума функции.

        Parameters:
        - max_iterations: максимальное число итераций

        Returns:
        - x, y: найденные координаты максимума
        - value: значение функции в точке максимума
        - history: история оптимизации
        - time_elapsed: время выполнения алгоритма
        """
        start_time = time.time()
        x, y = self.start_x, self.start_y
        iteration = 0
        history = []

        while iteration < max_iterations:
            old_value = self.func(x, y)
            history.append((x, y, old_value))

            # Вычисление градиента и матрицы Гессе
            gradient_x, gradient_y = self._compute_gradient(x, y)
            hessian_xx, hessian_yy, hessian_xy = self._compute_hessian(x, y)

            # Определитель матрицы Гессе
            det_hessian = hessian_xx * hessian_yy - hessian_xy ** 2

            # Для поиска максимума матрица Гессе должна быть отрицательно определена
            if abs(det_hessian) < 1e-10:
                # Если определитель близок к нулю, используем небольшой шаг по градиенту
                x = x + 0.01 * gradient_x
                y = y + 0.01 * gradient_y
            else:
                # Обновляем координаты с использованием метода Ньютона
                delta_x = (hessian_yy * gradient_x - hessian_xy * gradient_y) / det_hessian
                delta_y = (hessian_xx * gradient_y - hessian_xy * gradient_x) / det_hessian

                # Для поиска максимума используем противоположное направление
                x = x + delta_x
                y = y + delta_y

            new_value = self.func(x, y)

            # Проверка сходимости
            if abs(new_value - old_value) < self.tolerance:
                break

            iteration += 1

        time_elapsed = time.time() - start_time
        return x, y, self.func(x, y), history, time_elapsed


def visualize_optimization(func, history, title):
    """
    Визуализация функции и пути оптимизации.

    Parameters:
    - func: оптимизируемая функция
    - history: история оптимизации
    - title: заголовок графика

    Returns:
    - fig: фигура matplotlib
    """
    # Создаем сетку
    x = np.linspace(-1, 5, 100)
    y = np.linspace(-1, 5, 100)
    X, Y = np.meshgrid(x, y)
    Z = np.zeros_like(X)

    # Вычисляем значения функции
    for i in range(X.shape[0]):
        for j in range(X.shape[1]):
            Z[i, j] = func(X[i, j], Y[i, j])

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


def main():
    """Основная функция программы"""

    # Определение целевой функции
    def target_function(x, y):
        return (1 / (1 + ((x - 2) / 3) ** 2 + ((y - 2) / 3) ** 2)) + (3 / (1 + (x - 1) ** 2 + ((y - 1) / 2) ** 2))

    # Начальная точка
    start_x, start_y = 0.0, 0.0

    # Создание оптимизатора
    optimizer = FunctionOptimizer(target_function, start_x, start_y)

    # Запуск метода Гаусса
    gauss_x, gauss_y, gauss_value, gauss_history, gauss_time = optimizer.gauss_method()
    print("\nРезультаты метода Гаусса:")
    print(f"Точка максимума: x = {gauss_x:.6f}, y = {gauss_y:.6f}")
    print(f"Значение функции: f(x,y) = {gauss_value:.6f}")
    print(f"Количество итераций: {len(gauss_history)}")
    print(f"Время выполнения: {gauss_time:.6f} секунд")

    # Визуализация для метода Гаусса
    gauss_fig = visualize_optimization(target_function, gauss_history, "Метод Гаусса")

    # Запуск метода Ньютона
    newton_x, newton_y, newton_value, newton_history, newton_time = optimizer.newton_method()
    print("\nРезультаты метода Ньютона:")
    print(f"Точка максимума: x = {newton_x:.6f}, y = {newton_y:.6f}")
    print(f"Значение функции: f(x,y) = {newton_value:.6f}")
    print(f"Количество итераций: {len(newton_history)}")
    print(f"Время выполнения: {newton_time:.6f} секунд")

    # Визуализация для метода Ньютона
    newton_fig = visualize_optimization(target_function, newton_history, "Метод Ньютона")

    plt.show()


if __name__ == "__main__":
    main()