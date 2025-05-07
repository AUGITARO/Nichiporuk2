import numpy as np
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D


# Определение целевой функции
def objective_function(x, y):
    return 10 * (y - x) ** 2 + y ** 2


# Функция ограничения преобразованная так, чтобы g(x,y) > 0
# Ограничение x = 2 - y преобразуем в g(x,y) = (2 - y) - x
# Тогда g(x,y) > 0 означает x < 2 - y
def constraint(x, y):
    return (2 - y) - x


# Барьерная функция, которая стремится к бесконечности при приближении к границе допустимой области
def barrier_function(x, y, mu):
    constr_val = constraint(x, y)
    # Проверка, что мы находимся в допустимой области
    if constr_val <= 0:
        return float('inf')  # За пределами допустимой области возвращаем бесконечность
    return objective_function(x, y) - mu * np.log(constr_val)


# Начальные параметры
# Начальная точка должна быть внутри допустимой области (g(x,y) > 0)
x = 0.0
y = 0.0
mu = 1.0  # начальный параметр барьера
alpha = 0.01  # шаг для координатного спуска
epsilon = 1e-6  # точность
mu_reduction_factor = 0.1  # множитель для уменьшения параметра барьера
max_iterations = 1000  # максимальное число итераций
max_inner_iterations = 100  # максимальное число внутренних итераций

# История для визуализации
x_history = []
y_history = []
f_history = []

# Проверка, что начальная точка находится в допустимой области
if constraint(x, y) <= 0:
    # Если начальная точка не подходит, находим подходящую точку
    for test_x in np.linspace(-1, 1, 20):
        for test_y in np.linspace(-1, 1, 20):
            if constraint(test_x, test_y) > 0:
                x = test_x
                y = test_y
                break
        if constraint(x, y) > 0:
            break

# Внешний цикл - уменьшение параметра барьера
iteration = 0
converged = False

while not converged and iteration < max_iterations:
    # Внутренний цикл - поиск минимума текущей барьерной функции
    inner_iteration = 0
    inner_converged = False

    while not inner_converged and inner_iteration < max_inner_iterations:
        # Добавляем текущую точку в историю
        x_history.append(x)
        y_history.append(y)
        f_history.append(objective_function(x, y))

        # Текущее значение барьерной функции
        current_value = barrier_function(x, y, mu)

        # Расчет направления поиска (метод координатного спуска - 0-го порядка)
        # Сначала делаем пробный шаг по x
        x_plus = x + alpha
        x_minus = x - alpha

        # Проверяем, что пробные точки находятся в допустимой области
        value_plus_x = barrier_function(x_plus, y, mu)
        value_minus_x = barrier_function(x_minus, y, mu)

        # Выбираем лучшее направление по x
        if value_plus_x < current_value and value_plus_x < value_minus_x:
            x = x_plus
        elif value_minus_x < current_value:
            x = x_minus

        # Обновляем текущее значение после шага по x
        current_value = barrier_function(x, y, mu)

        # Затем делаем пробный шаг по y
        y_plus = y + alpha
        y_minus = y - alpha

        # Проверяем, что пробные точки находятся в допустимой области
        value_plus_y = barrier_function(x, y_plus, mu)
        value_minus_y = barrier_function(x, y_minus, mu)

        # Выбираем лучшее направление по y
        if value_plus_y < current_value and value_plus_y < value_minus_y:
            y = y_plus
        elif value_minus_y < current_value:
            y = y_minus

        # Проверяем условие сходимости внутреннего цикла
        new_value = barrier_function(x, y, mu)
        if abs(current_value - new_value) < epsilon:
            inner_converged = True

        inner_iteration += 1

    # Проверка условия сходимости внешнего цикла
    if mu < epsilon:
        converged = True
    else:
        # Уменьшаем параметр барьера
        mu *= mu_reduction_factor

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

# Заштриховываем недопустимую область (x > 2 - y)
invalid_x = np.linspace(-1, 3, 100)
invalid_y = np.linspace(-1, 3, 100)
invalid_X, invalid_Y = np.meshgrid(invalid_x, invalid_y)
invalid_mask = invalid_X > (2 - invalid_Y)
ax2.contourf(invalid_X, invalid_Y, invalid_mask.astype(float), levels=[0.5, 1.5], colors='gray', alpha=0.3)

# Отображаем путь оптимизации
ax2.plot(x_history, y_history, 'b-', alpha=0.6)
ax2.scatter(x_history, y_history, color='b', s=10, alpha=0.6)
ax2.scatter(x, y, color='r', s=100, marker='*', label='Минимум')

ax2.legend()
plt.colorbar(contour, ax=ax2)
plt.tight_layout()
plt.show()
