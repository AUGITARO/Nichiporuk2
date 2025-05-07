import numpy as np
import matplotlib.pyplot as plt
import random
import time
from typing import Tuple, List, Callable

# Начало измерения времени
start_time = time.time()

# Параметры функции
C = np.array([1, 1.2, 3, 3.2, 5, 5])
a = np.array([4, -4, 4, -4, 0, 0])
b = np.array([4, 4, -4, -4, 0, 0])

# Границы поиска
BOUNDS = (-10, 10)


def objective_function(x: float, y: float) -> float:
    """
    Целевая функция для оптимизации
    f(x, y) = Σ [C_i / (1 + (x - a_i)^2 + (y - b_i)^2)] для i=1..6
    """
    denominators = 1 + (x - a) ** 2 + (y - b) ** 2
    return np.sum(C / denominators)


def clip_to_bounds(point: Tuple[float, float]) -> Tuple[float, float]:
    """Ограничивает координаты точки в пределах заданных границ"""
    x, y = point
    return (
        max(BOUNDS[0], min(BOUNDS[1], x)),
        max(BOUNDS[0], min(BOUNDS[1], y))
    )


def random_search(num_iterations: int) -> Tuple[float, float, float]:
    """
    Реализация метода простого случайного поиска

    Args:
        num_iterations: количество итераций

    Returns:
        Tuple из (лучшее_значение, x_координата, y_координата)
    """
    best_value = float('-inf')
    best_point = (0, 0)

    for _ in range(num_iterations):
        x = random.uniform(BOUNDS[0], BOUNDS[1])
        y = random.uniform(BOUNDS[0], BOUNDS[1])
        value = objective_function(x, y)

        if value > best_value:
            best_value = value
            best_point = (x, y)

    return best_value, best_point[0], best_point[1]


def simulated_annealing(num_iterations: int,
                        initial_temp: float = 10.0,
                        cooling_rate: float = 0.95) -> Tuple[float, float, float]:
    """
    Метод имитации отжига для поиска глобального максимума

    Args:
        num_iterations: количество итераций
        initial_temp: начальная температура
        cooling_rate: коэффициент охлаждения

    Returns:
        Tuple из (лучшее_значение, x_координата, y_координата)
    """
    # Инициализация случайной начальной точки
    current_point = (
        random.uniform(BOUNDS[0], BOUNDS[1]),
        random.uniform(BOUNDS[0], BOUNDS[1])
    )
    current_value = objective_function(*current_point)

    best_point = current_point
    best_value = current_value
    temp = initial_temp

    for _ in range(num_iterations):
        # Генерация нового кандидата в окрестности текущего решения
        new_point = (
            current_point[0] + random.uniform(-1, 1),
            current_point[1] + random.uniform(-1, 1)
        )
        new_point = clip_to_bounds(new_point)
        new_value = objective_function(*new_point)

        # Критерий принятия решения
        if new_value > current_value:
            current_point = new_point
            current_value = new_value
        else:
            # Принятие худшего решения с некоторой вероятностью
            p = np.exp((new_value - current_value) / temp)
            if random.random() < p:
                current_point = new_point
                current_value = new_value

        # Обновление лучшего решения
        if current_value > best_value:
            best_value = current_value
            best_point = current_point

        # Снижение температуры
        temp *= cooling_rate

    return best_value, best_point[0], best_point[1]


def genetic_algorithm(population_size: int = 50,
                      num_generations: int = 20,
                      mutation_rate: float = 0.1) -> Tuple[float, float, float]:
    """
    Генетический алгоритм для поиска глобального максимума

    Args:
        population_size: размер популяции
        num_generations: количество поколений
        mutation_rate: вероятность мутации

    Returns:
        Tuple из (лучшее_значение, x_координата, y_координата)
    """
    # Создаем начальную популяцию
    population = []
    for _ in range(population_size):
        x = random.uniform(BOUNDS[0], BOUNDS[1])
        y = random.uniform(BOUNDS[0], BOUNDS[1])
        fitness = objective_function(x, y)
        population.append((x, y, fitness))

    for _ in range(num_generations):
        # Сортировка по приспособленности (по убыванию)
        population.sort(key=lambda ind: ind[2], reverse=True)

        # Выбор элиты (лучшая половина популяции)
        elite = population[:population_size // 2]

        # Создание нового поколения
        new_population = elite.copy()

        # Скрещивание и мутация для создания потомков
        while len(new_population) < population_size:
            parent1 = random.choice(elite)
            parent2 = random.choice(elite)

            # Скрещивание (кроссовер)
            child_x = (parent1[0] + parent2[0]) / 2
            child_y = (parent1[1] + parent2[1]) / 2

            # Мутация
            if random.random() < mutation_rate:
                child_x += random.uniform(-1, 1)
            if random.random() < mutation_rate:
                child_y += random.uniform(-1, 1)

            # Ограничение в пределах границ
            child_x, child_y = clip_to_bounds((child_x, child_y))

            # Оценка приспособленности
            child_fitness = objective_function(child_x, child_y)
            new_population.append((child_x, child_y, child_fitness))

        population = new_population

    # Находим лучшую особь
    best_individual = max(population, key=lambda ind: ind[2])
    return best_individual[2], best_individual[0], best_individual[1]


def particle_swarm_optimization(num_particles: int = 30,
                                max_iterations: int = 50,
                                w: float = 0.5,
                                c1: float = 1.5,
                                c2: float = 1.5) -> Tuple[float, float, float]:
    """
    Метод роя частиц для поиска глобального максимума

    Args:
        num_particles: количество частиц
        max_iterations: максимальное количество итераций
        w: инерционный вес
        c1: когнитивный параметр
        c2: социальный параметр

    Returns:
        Tuple из (лучшее_значение, x_координата, y_координата)
    """
    # Инициализация частиц
    particles = []
    for _ in range(num_particles):
        x = random.uniform(BOUNDS[0], BOUNDS[1])
        y = random.uniform(BOUNDS[0], BOUNDS[1])
        velocity_x = random.uniform(-1, 1)
        velocity_y = random.uniform(-1, 1)
        fitness = objective_function(x, y)

        particles.append({
            'position': (x, y),
            'velocity': (velocity_x, velocity_y),
            'fitness': fitness,
            'best_position': (x, y),
            'best_fitness': fitness
        })

    # Инициализация глобального лучшего
    global_best = max(particles, key=lambda p: p['best_fitness'])
    global_best_position = global_best['best_position']
    global_best_fitness = global_best['best_fitness']

    # Основной цикл PSO
    for _ in range(max_iterations):
        for particle in particles:
            # Обновление скорости
            r1, r2 = random.random(), random.random()

            new_vel_x = (w * particle['velocity'][0] +
                         c1 * r1 * (particle['best_position'][0] - particle['position'][0]) +
                         c2 * r2 * (global_best_position[0] - particle['position'][0]))

            new_vel_y = (w * particle['velocity'][1] +
                         c1 * r1 * (particle['best_position'][1] - particle['position'][1]) +
                         c2 * r2 * (global_best_position[1] - particle['position'][1]))

            particle['velocity'] = (new_vel_x, new_vel_y)

            # Обновление позиции
            new_pos_x = particle['position'][0] + particle['velocity'][0]
            new_pos_y = particle['position'][1] + particle['velocity'][1]

            # Ограничение координат
            new_pos_x, new_pos_y = clip_to_bounds((new_pos_x, new_pos_y))
            particle['position'] = (new_pos_x, new_pos_y)

            # Оценка новой позиции
            particle['fitness'] = objective_function(*particle['position'])

            # Обновление лучшей позиции частицы
            if particle['fitness'] > particle['best_fitness']:
                particle['best_fitness'] = particle['fitness']
                particle['best_position'] = particle['position']

                # Обновление глобального лучшего
                if particle['best_fitness'] > global_best_fitness:
                    global_best_fitness = particle['best_fitness']
                    global_best_position = particle['best_position']

    return global_best_fitness, global_best_position[0], global_best_position[1]


def run_and_compare_algorithms() -> List[Tuple[str, float, float, float]]:
    """
    Запускает все алгоритмы оптимизации и возвращает их результаты

    Returns:
        Список кортежей (название_алгоритма, лучшее_значение, x, y)
    """
    print("Запуск алгоритмов оптимизации...")

    # Параметры для всех алгоритмов
    num_iterations = 1000

    # Запуск случайного поиска
    random_value, random_x, random_y = random_search(num_iterations)
    print(f"\nМетод случайного поиска:")
    print(f"Максимальное значение: {random_value}")
    print(f"Координаты: x = {random_x}, y = {random_y}")

    # Запуск имитации отжига
    sa_value, sa_x, sa_y = simulated_annealing(num_iterations)
    print(f"\nМетод имитации отжига:")
    print(f"Максимальное значение: {sa_value}")
    print(f"Координаты: x = {sa_x}, y = {sa_y}")

    # Запуск генетического алгоритма
    ga_value, ga_x, ga_y = genetic_algorithm()
    print(f"\nГенетический алгоритм:")
    print(f"Максимальное значение: {ga_value}")
    print(f"Координаты: x = {ga_x}, y = {ga_y}")

    # Запуск метода роя частиц
    pso_value, pso_x, pso_y = particle_swarm_optimization()
    print(f"\nМетод роя частиц:")
    print(f"Максимальное значение: {pso_value}")
    print(f"Координаты: x = {pso_x}, y = {pso_y}")

    # Формирование результатов
    results = [
        ("Случайный поиск", random_value, random_x, random_y),
        ("Имитация отжига", sa_value, sa_x, sa_y),
        ("Генетический алгоритм", ga_value, ga_x, ga_y),
        ("Метод роя частиц", pso_value, pso_x, pso_y)
    ]

    return results


def visualize_results(results: List[Tuple[str, float, float, float]]) -> None:
    """
    Визуализирует функцию и найденные точки максимума

    Args:
        results: список результатов всех алгоритмов
    """
    print("\nВизуализация результатов...")

    # Создание сетки для построения графика функции
    x = np.linspace(BOUNDS[0], BOUNDS[1], 100)
    y = np.linspace(BOUNDS[0], BOUNDS[1], 100)
    X, Y = np.meshgrid(x, y)

    # Векторизованное вычисление значений функции
    Z = np.zeros_like(X)
    for i in range(len(X)):
        for j in range(len(X[0])):
            Z[i, j] = objective_function(X[i, j], Y[i, j])

    # Настройка графика
    plt.figure(figsize=(12, 10))
    contour = plt.contourf(X, Y, Z, 50, cmap='viridis')
    plt.colorbar(contour, label='f(x, y)')

    # Отметка найденных максимумов
    colors = ['red', 'blue', 'green', 'purple']
    markers = ['o', 's', '^', 'x']

    for i, (name, value, x, y) in enumerate(results):
        plt.scatter(x, y, color=colors[i], marker=markers[i], s=100,
                    label=f'{name}: {value:.4f} в точке ({x:.4f}, {y:.4f})')

    plt.title('Сравнение алгоритмов поиска глобального максимума')
    plt.xlabel('x')
    plt.ylabel('y')
    plt.legend(loc='upper left', bbox_to_anchor=(1, 1))
    plt.grid(True)
    plt.tight_layout()
    plt.savefig('optimized_comparison.png')
    plt.show()


def main():
    """Основная функция программы"""
    # Запуск всех алгоритмов и получение результатов
    results = run_and_compare_algorithms()

    # Определение лучшего алгоритма
    best_algorithm = max(results, key=lambda x: x[1])
    print("\nНаилучший результат:")
    print(f"Алгоритм: {best_algorithm[0]}")
    print(f"Максимальное значение: {best_algorithm[1]}")
    print(f"Координаты: x = {best_algorithm[2]}, y = {best_algorithm[3]}")

    # Визуализация результатов
    visualize_results(results)

    # Измерение общего времени выполнения
    end_time = time.time()
    print(f"\nВремя выполнения: {end_time - start_time:.4f} секунд")


if __name__ == "__main__":
    main()
