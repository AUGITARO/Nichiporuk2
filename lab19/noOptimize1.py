import numpy as np
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D


# Определение целевой функции и функции ограничения
def objective_function(x, y):
    return 10 * (y - x) ** 2 + y ** 2


def constraint(x, y):
    return x - (2 - y)


# Метод штрафных функций
# Функция с штрафом: F(x,y) = f(x,y) + r*g(x,y)^2, где g(x,y) - функция ограничения
def penalty_function(x, y, r):
    return objective_function(x, y) + r * constraint(x, y) ** 2


# Начальные параметры
x = 0.0
y = 0.0
r = 1.0  # начальный коэффициент штрафа
alpha = 0.01  # шаг для градиентного спуска
epsilon = 1e-6  # точность
beta = 10.0  # множитель для увеличения штрафа
max_iterations = 10000  # максимальное число итераций
max_inner_iterations = 100  # максимальное число внутренних итераций

# История для визуализации
x_history = []
y_history = []
f_history = []

# Внешний цикл - увеличение штрафа
iteration = 0
converged = False

while not converged and iteration < max_iterations:
    # Внутренний цикл - поиск минимума текущей штрафной функции
    inner_iteration = 0
    inner_converged = False

    while not inner_converged and inner_iteration < max_inner_iterations:
        # Добавляем текущую точку в историю
        x_history.append(x)
        y_history.append(y)
        f_history.append(objective_function(x, y))

        # Расчет направления поиска (метод координатного спуска - 0-го порядка)
        # Сначала делаем пробный шаг по x
        x_test = x + alpha
        if penalty_function(x_test, y, r) < penalty_function(x, y, r):
            x = x_test
        else:
            x_test = x - alpha
            if penalty_function(x_test, y, r) < penalty_function(x, y, r):
                x = x_test

        # Затем делаем пробный шаг по y
        y_test = y + alpha
        if penalty_function(x, y_test, r) < penalty_function(x, y, r):
            y = y_test
        else:
            y_test = y - alpha
            if penalty_function(x, y_test, r) < penalty_function(x, y, r):
                y = y_test

        # Проверяем условие сходимости внутреннего цикла
        current_value = penalty_function(x, y, r)
        next_x = x + alpha if penalty_function(x + alpha, y, r) < penalty_function(x - alpha, y, r) else x - alpha
        next_y = y + alpha if penalty_function(x, y + alpha, r) < penalty_function(x, y - alpha, r) else y - alpha
        next_value = penalty_function(next_x, next_y, r)

        if abs(current_value - next_value) < epsilon:
            inner_converged = True

        inner_iteration += 1

    # Проверка сходимости по ограничению
    if abs(constraint(x, y)) < epsilon:
        converged = True
    else:
        # Увеличиваем коэффициент штрафа
        r *= beta

    iteration += 1

# Добавляем финальную точку в историю
x_history.append(x)
y_history.append(y)
f_history.append(objective_function(x, y))

# Вывод результатов
print(f"Найденная точка минимума: x = {x:.6f}, y = {y:.6f}")
print(f"Значение функции: f(x,y) = {objective_function(x, y):.6f}")
print(f"Значение ограничения: g(x,y) = {constraint(x, y):.6f}")
print(f"Количество итераций: {iteration}")

# Визуализация результатов
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
path_z = [objective_function(x, y) for x, y in zip(x_history, y_history)]
ax1.scatter(x_history, y_history, path_z, color='r', s=10, alpha=0.6)

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
ax2.plot(x_history, y_history, 'b-', alpha=0.6)
ax2.scatter(x_history, y_history, color='b', s=10, alpha=0.6)
ax2.scatter(x, y, color='r', s=100, marker='*', label='Минимум')

ax2.legend()
plt.colorbar(contour, ax=ax2)
plt.tight_layout()
plt.show()
