import numpy as np
import matplotlib.pyplot as plt
import random
import time

# Начало измерения времени
start_time = time.time()

# Параметры функции
C = [1, 1.2, 3, 3.2, 5, 5]
a = [4, -4, 4, -4, 0, 0]
b = [4, 4, -4, -4, 0, 0]

# Параметры алгоритмов
num_iterations = 1000  # Количество итераций
x_min, x_max = -10, 10  # Границы для x
y_min, y_max = -10, 10  # Границы для y


# Функция, которую оптимизируем
def f(x, y):
    result = 0
    for i in range(6):
        result = result + C[i] / (1 + (x - a[i]) ** 2 + (y - b[i]) ** 2)
    return result


# Простой случайный поиск
max_value_random = -float('inf')
max_x_random = 0
max_y_random = 0

for i in range(num_iterations):
    x = random.uniform(x_min, x_max)
    y = random.uniform(y_min, y_max)
    value = f(x, y)

    if value > max_value_random:
        max_value_random = value
        max_x_random = x
        max_y_random = y

print("Метод случайного поиска:")
print(f"Максимальное значение: {max_value_random}")
print(f"Координаты: x = {max_x_random}, y = {max_y_random}")

# Алгоритм имитации отжига
current_x = random.uniform(x_min, x_max)
current_y = random.uniform(y_min, y_max)
current_value = f(current_x, current_y)
best_x = current_x
best_y = current_y
best_value = current_value
temp = 10.0  # Начальная температура

for i in range(num_iterations):
    # Генерация нового решения в окрестности текущего
    new_x = current_x + random.uniform(-1, 1)
    new_y = current_y + random.uniform(-1, 1)

    # Проверка границ
    if new_x < x_min:
        new_x = x_min
    if new_x > x_max:
        new_x = x_max
    if new_y < y_min:
        new_y = y_min
    if new_y > y_max:
        new_y = y_max

    new_value = f(new_x, new_y)

    # Вероятность принятия худшего решения
    if new_value > current_value:
        current_x = new_x
        current_y = new_y
        current_value = new_value
    else:
        p = np.exp((new_value - current_value) / temp)
        if random.random() < p:
            current_x = new_x
            current_y = new_y
            current_value = new_value

    # Обновление лучшего решения
    if current_value > best_value:
        best_x = current_x
        best_y = current_y
        best_value = current_value

    # Снижение температуры
    temp = temp * 0.95

print("\nМетод имитации отжига:")
print(f"Максимальное значение: {best_value}")
print(f"Координаты: x = {best_x}, y = {best_y}")

# Генетический алгоритм
population_size = 50
mutation_rate = 0.1
num_generations = 20

# Инициализация популяции
population = []
for i in range(population_size):
    x = random.uniform(x_min, x_max)
    y = random.uniform(y_min, y_max)
    fitness = f(x, y)
    population.append((x, y, fitness))

for generation in range(num_generations):
    # Сортировка популяции по приспособленности
    population.sort(key=lambda ind: ind[2], reverse=True)

    # Выбор лучших особей
    elite = population[:population_size // 2]

    # Создание нового поколения
    new_population = elite.copy()

    # Создание потомков через кроссовер
    while len(new_population) < population_size:
        parent1 = random.choice(elite)
        parent2 = random.choice(elite)

        # Кроссовер
        child_x = (parent1[0] + parent2[0]) / 2
        child_y = (parent1[1] + parent2[1]) / 2

        # Мутация
        if random.random() < mutation_rate:
            child_x = child_x + random.uniform(-1, 1)
        if random.random() < mutation_rate:
            child_y = child_y + random.uniform(-1, 1)

        # Проверка границ
        if child_x < x_min:
            child_x = x_min
        if child_x > x_max:
            child_x = x_max
        if child_y < y_min:
            child_y = y_min
        if child_y > y_max:
            child_y = y_max

        child_fitness = f(child_x, child_y)
        new_population.append((child_x, child_y, child_fitness))

    population = new_population

# Нахождение лучшего индивида
best_individual = max(population, key=lambda ind: ind[2])

print("\nГенетический алгоритм:")
print(f"Максимальное значение: {best_individual[2]}")
print(f"Координаты: x = {best_individual[0]}, y = {best_individual[1]}")

# Метод роя частиц
num_particles = 30
max_iterations = 50
w = 0.5  # Инерционный вес
c1 = 1.5  # Когнитивный параметр
c2 = 1.5  # Социальный параметр

# Инициализация частиц
particles = []
for i in range(num_particles):
    x = random.uniform(x_min, x_max)
    y = random.uniform(y_min, y_max)
    velocity_x = random.uniform(-1, 1)
    velocity_y = random.uniform(-1, 1)
    fitness = f(x, y)
    best_x = x
    best_y = y
    best_fitness = fitness
    particles.append([x, y, velocity_x, velocity_y, fitness, best_x, best_y, best_fitness])

# Глобальное лучшее положение
global_best_x = particles[0][5]
global_best_y = particles[0][6]
global_best_fitness = particles[0][7]

for particle in particles:
    if particle[7] > global_best_fitness:
        global_best_fitness = particle[7]
        global_best_x = particle[5]
        global_best_y = particle[6]

# Основной цикл метода
for iteration in range(max_iterations):
    for i in range(num_particles):
        # Обновление скорости
        r1 = random.random()
        r2 = random.random()

        particles[i][2] = w * particles[i][2] + c1 * r1 * (particles[i][5] - particles[i][0]) + c2 * r2 * (
                    global_best_x - particles[i][0])
        particles[i][3] = w * particles[i][3] + c1 * r1 * (particles[i][6] - particles[i][1]) + c2 * r2 * (
                    global_best_y - particles[i][1])

        # Обновление позиции
        particles[i][0] += particles[i][2]
        particles[i][1] += particles[i][3]

        # Проверка границ
        if particles[i][0] < x_min:
            particles[i][0] = x_min
        if particles[i][0] > x_max:
            particles[i][0] = x_max
        if particles[i][1] < y_min:
            particles[i][1] = y_min
        if particles[i][1] > y_max:
            particles[i][1] = y_max

        # Вычисление новой приспособленности
        particles[i][4] = f(particles[i][0], particles[i][1])

        # Обновление личного лучшего
        if particles[i][4] > particles[i][7]:
            particles[i][7] = particles[i][4]
            particles[i][5] = particles[i][0]
            particles[i][6] = particles[i][1]

            # Обновление глобального лучшего
            if particles[i][7] > global_best_fitness:
                global_best_fitness = particles[i][7]
                global_best_x = particles[i][5]
                global_best_y = particles[i][6]

print("\nМетод роя частиц:")
print(f"Максимальное значение: {global_best_fitness}")
print(f"Координаты: x = {global_best_x}, y = {global_best_y}")

# Общее сравнение результатов всех алгоритмов
results = [
    ("Случайный поиск", max_value_random, max_x_random, max_y_random),
    ("Имитация отжига", best_value, best_x, best_y),
    ("Генетический алгоритм", best_individual[2], best_individual[0], best_individual[1]),
    ("Метод роя частиц", global_best_fitness, global_best_x, global_best_y)
]

best_algorithm = max(results, key=lambda x: x[1])
print("\nНаилучший результат:")
print(f"Алгоритм: {best_algorithm[0]}")
print(f"Максимальное значение: {best_algorithm[1]}")
print(f"Координаты: x = {best_algorithm[2]}, y = {best_algorithm[3]}")

# Завершение измерения времени
end_time = time.time()
print(f"\nВремя выполнения: {end_time - start_time:.4f} секунд")

# Визуализация функции и найденных точек максимума
x = np.linspace(x_min, x_max, 100)
y = np.linspace(y_min, y_max, 100)
X, Y = np.meshgrid(x, y)
Z = np.zeros_like(X)

for i in range(len(X)):
    for j in range(len(X[0])):
        Z[i][j] = f(X[i][j], Y[i][j])

plt.figure(figsize=(10, 8))
plt.contourf(X, Y, Z, 50, cmap='viridis')
plt.colorbar(label='f(x, y)')

# Отметим найденные точки максимума
colors = ['red', 'blue', 'green', 'purple']
markers = ['o', 's', '^', 'x']
labels = ['Случайный поиск', 'Имитация отжига', 'Генетический алгоритм', 'Метод роя частиц']

for i, (alg, val, x, y) in enumerate(results):
    plt.scatter(x, y, color=colors[i], marker=markers[i], s=100, label=f'{labels[i]}: {val:.4f}')

plt.title('Поиск глобального максимума функции f(x, y)')
plt.xlabel('x')
plt.ylabel('y')
plt.legend()
plt.grid(True)
plt.savefig('global_optimization_comparison.png')
plt.show()
