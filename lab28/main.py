import tkinter as tk
from tkinter import ttk, messagebox
import numpy as np
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
import random
import time
import threading


class OptimizationApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Global Optimization Toolkit")
        self.root.geometry("1200x800")

        # Параметры функции
        self.C = [1, 1.2, 3, 3.2, 5, 5]
        self.a = [4, -4, 4, -4, 0, 0]
        self.b = [4, 4, -4, -4, 0, 0]

        self.create_widgets()
        self.set_default_values()

    def create_widgets(self):
        # Панель параметров
        params_frame = ttk.LabelFrame(self.root, text="Параметры оптимизации")
        params_frame.pack(side=tk.LEFT, padx=10, pady=10, fill=tk.Y)

        # Общие параметры
        ttk.Label(params_frame, text="Общие параметры:").grid(row=0, column=0, columnspan=2, pady=5)

        self.inputs = {
            'x_min': self.create_param_entry(params_frame, "X min:", 1, -10),
            'x_max': self.create_param_entry(params_frame, "X max:", 2, 10),
            'y_min': self.create_param_entry(params_frame, "Y min:", 3, -10),
            'y_max': self.create_param_entry(params_frame, "Y max:", 4, 10),
            'iterations': self.create_param_entry(params_frame, "Число итераций:", 5, 1000)
        }

        # Параметры алгоритмов
        algo_frame = ttk.LabelFrame(params_frame, text="Выбор алгоритмов")
        algo_frame.grid(row=6, column=0, columnspan=2, pady=10, sticky=tk.W)

        self.algorithms = {
            'random_search': tk.BooleanVar(value=True),
            'simulated_annealing': tk.BooleanVar(value=True),
            'genetic_algorithm': tk.BooleanVar(value=True),
            'particle_swarm': tk.BooleanVar(value=True)
        }

        ttk.Checkbutton(algo_frame, text="Случайный поиск", variable=self.algorithms['random_search']).pack(anchor=tk.W)
        ttk.Checkbutton(algo_frame, text="Имитация отжига", variable=self.algorithms['simulated_annealing']).pack(
            anchor=tk.W)
        ttk.Checkbutton(algo_frame, text="Генетический алгоритм", variable=self.algorithms['genetic_algorithm']).pack(
            anchor=tk.W)
        ttk.Checkbutton(algo_frame, text="Метод роя частиц", variable=self.algorithms['particle_swarm']).pack(
            anchor=tk.W)

        # Кнопки управления
        btn_frame = ttk.Frame(params_frame)
        btn_frame.grid(row=7, column=0, columnspan=2, pady=10)

        ttk.Button(btn_frame, text="Запуск", command=self.start_optimization).pack(side=tk.LEFT, padx=5)
        ttk.Button(btn_frame, text="Сброс", command=self.set_default_values).pack(side=tk.LEFT, padx=5)

        # Область результатов
        result_frame = ttk.LabelFrame(self.root, text="Результаты")
        result_frame.pack(side=tk.RIGHT, padx=10, pady=10, fill=tk.BOTH, expand=True)

        self.result_text = tk.Text(result_frame, height=15, width=60)
        self.result_text.pack(fill=tk.BOTH, expand=True)

        # График
        self.figure = plt.figure(figsize=(8, 6))
        self.canvas = FigureCanvasTkAgg(self.figure, master=result_frame)
        self.canvas.get_tk_widget().pack(fill=tk.BOTH, expand=True)

    def create_param_entry(self, parent, label, row, default):
        ttk.Label(parent, text=label).grid(row=row, column=0, sticky=tk.W, padx=5, pady=2)
        entry = ttk.Entry(parent, width=10)
        entry.grid(row=row, column=1, sticky=tk.E, padx=5, pady=2)
        entry.insert(0, str(default))
        return entry

    def set_default_values(self):
        defaults = {
            'x_min': -10,
            'x_max': 10,
            'y_min': -10,
            'y_max': 10,
            'iterations': 1000
        }
        for key, entry in self.inputs.items():
            entry.delete(0, tk.END)
            entry.insert(0, str(defaults.get(key, 0)))

        for algo in self.algorithms.values():
            algo.set(True)

        self.result_text.delete(1.0, tk.END)
        self.figure.clear()
        self.canvas.draw()

    def validate_inputs(self):
        try:
            params = {key: float(entry.get()) for key, entry in self.inputs.items()}
            params['iterations'] = int(params['iterations'])

            if not any(self.algorithms[algo].get() for algo in self.algorithms):
                raise ValueError("Выберите хотя бы один алгоритм")

            if params['x_min'] >= params['x_max']:
                raise ValueError("X min должен быть меньше X max")

            if params['y_min'] >= params['y_max']:
                raise ValueError("Y min должен быть меньше Y max")

            return params
        except ValueError as e:
            messagebox.showerror("Ошибка", f"Некорректный ввод: {str(e)}")
            return None

    def start_optimization(self):
        params = self.validate_inputs()
        if params:
            self.result_text.delete(1.0, tk.END)
            self.result_text.insert(tk.END, "Запуск оптимизации...\n")
            self.root.update()
            threading.Thread(target=self.run_optimization, args=(params,), daemon=True).start()

    def f(self, x, y):
        return sum(c / (1 + (x - ai) ** 2 + (y - bi) ** 2)
                   for c, ai, bi in zip(self.C, self.a, self.b))

    def run_optimization(self, params):
        start_time = time.time()
        results = []

        try:
            if self.algorithms['random_search'].get():
                results.append(self.run_random_search(params))

            if self.algorithms['simulated_annealing'].get():
                results.append(self.run_simulated_annealing(params))

            if self.algorithms['genetic_algorithm'].get():
                results.append(self.run_genetic_algorithm(params))

            if self.algorithms['particle_swarm'].get():
                results.append(self.run_particle_swarm(params))

            self.update_results(results)
            self.update_plot(results, params)

        except Exception as e:
            self.show_error(f"Ошибка выполнения: {str(e)}")

        finally:
            self.result_text.insert(tk.END, f"\nОбщее время выполнения: {time.time() - start_time:.2f} сек")

    def run_random_search(self, params):
        max_value = -np.inf
        max_x = max_y = 0

        for _ in range(params['iterations']):
            x = random.uniform(params['x_min'], params['x_max'])
            y = random.uniform(params['y_min'], params['y_max'])
            value = self.f(x, y)

            if value > max_value:
                max_value = value
                max_x, max_y = x, y

        self.append_result("Случайный поиск", max_value, max_x, max_y)
        return ("Случайный поиск", max_value, max_x, max_y)

    def run_simulated_annealing(self, params):
        current_x = random.uniform(params['x_min'], params['x_max'])
        current_y = random.uniform(params['y_min'], params['y_max'])
        current_value = self.f(current_x, current_y)
        best_x, best_y, best_value = current_x, current_y, current_value
        temp = 10.0

        for _ in range(params['iterations']):
            new_x = current_x + random.uniform(-1, 1)
            new_y = current_y + random.uniform(-1, 1)
            new_x = np.clip(new_x, params['x_min'], params['x_max'])
            new_y = np.clip(new_y, params['y_min'], params['y_max'])

            new_value = self.f(new_x, new_y)

            if new_value > current_value or random.random() < np.exp((new_value - current_value) / temp):
                current_x, current_y, current_value = new_x, new_y, new_value

            if current_value > best_value:
                best_x, best_y, best_value = current_x, current_y, current_value

            temp *= 0.95

        self.append_result("Имитация отжига", best_value, best_x, best_y)
        return ("Имитация отжига", best_value, best_x, best_y)

    def run_genetic_algorithm(self, params):
        population_size = 50
        num_generations = 20
        mutation_rate = 0.1

        population = [
            (random.uniform(params['x_min'], params['x_max']),
             random.uniform(params['y_min'], params['y_max']))
            for _ in range(population_size)
        ]

        for _ in range(num_generations):
            population = sorted(population, key=lambda p: -self.f(p[0], p[1]))
            elite = population[:population_size // 2]

            new_population = elite.copy()
            while len(new_population) < population_size:
                p1, p2 = random.choices(elite, k=2)
                child = (
                    (p1[0] + p2[0]) / 2 + random.uniform(-1, 1) * mutation_rate,
                    (p1[1] + p2[1]) / 2 + random.uniform(-1, 1) * mutation_rate
                )
                child = (
                    np.clip(child[0], params['x_min'], params['x_max']),
                    np.clip(child[1], params['y_min'], params['y_max'])
                )
                new_population.append(child)

            population = new_population

        best = max(population, key=lambda p: self.f(p[0], p[1]))
        best_value = self.f(*best)

        self.append_result("Генетический алгоритм", best_value, best[0], best[1])
        return ("Генетический алгоритм", best_value, best[0], best[1])

    def run_particle_swarm(self, params):
        num_particles = 30
        max_iterations = 50
        w = 0.5
        c1 = c2 = 1.5

        particles = [
            (random.uniform(params['x_min'], params['x_max']),
             random.uniform(params['y_min'], params['y_max']),
             random.uniform(-1, 1),
             random.uniform(-1, 1))
            for _ in range(num_particles)
        ]

        global_best = max(particles, key=lambda p: self.f(p[0], p[1]))
        global_best_value = self.f(global_best[0], global_best[1])

        for _ in range(max_iterations):
            for i in range(num_particles):
                x, y, vx, vy = particles[i]

                # Обновление скорости
                vx = w * vx + c1 * random.random() * (global_best[0] - x) + c2 * random.random() * (global_best[0] - x)
                vy = w * vy + c1 * random.random() * (global_best[1] - y) + c2 * random.random() * (global_best[1] - y)

                # Обновление позиции
                x = np.clip(x + vx, params['x_min'], params['x_max'])
                y = np.clip(y + vy, params['y_min'], params['y_max'])

                # Обновление глобального максимума
                current_value = self.f(x, y)
                if current_value > global_best_value:
                    global_best = (x, y)
                    global_best_value = current_value

                particles[i] = (x, y, vx, vy)

        self.append_result("Метод роя частиц", global_best_value, global_best[0], global_best[1])
        return ("Метод роя частиц", global_best_value, global_best[0], global_best[1])

    def append_result(self, algorithm, value, x, y):
        text = (
            f"\n{algorithm}:\n"
            f"Максимальное значение: {value:.4f}\n"
            f"Координаты: ({x:.4f}, {y:.4f})\n"
            "--------------------------------"
        )
        self.result_text.after(0, self.result_text.insert, tk.END, text)

    def update_results(self, results):
        best = max(results, key=lambda x: x[1])
        text = (
            "\n\nНаилучший результат:\n"
            f"Алгоритм: {best[0]}\n"
            f"Значение: {best[1]:.4f}\n"
            f"Координаты: ({best[2]:.4f}, {best[3]:.4f})"
        )
        self.result_text.after(0, self.result_text.insert, tk.END, text)

    def update_plot(self, results, params):
        self.figure.clear()
        ax = self.figure.add_subplot(111)

        # Генерация сетки
        x = np.linspace(params['x_min'], params['x_max'], 100)
        y = np.linspace(params['y_min'], params['y_max'], 100)
        X, Y = np.meshgrid(x, y)
        Z = np.vectorize(self.f)(X, Y)

        # Отрисовка контурного графика
        cont = ax.contourf(X, Y, Z, 50, cmap='viridis')
        plt.colorbar(cont, ax=ax)

        # Отметки результатов
        colors = ['red', 'blue', 'green', 'purple']
        markers = ['o', 's', '^', 'D']

        for i, (name, value, x, y) in enumerate(results):
            ax.scatter(x, y, c=colors[i], marker=markers[i], s=100,
                       label=f"{name}: {value:.4f}")

        ax.set_title("Результаты оптимизации")
        ax.set_xlabel("X")
        ax.set_ylabel("Y")
        ax.legend()
        self.canvas.draw()

    def show_error(self, message):
        self.result_text.after(0, messagebox.showerror, "Ошибка", message)


if __name__ == "__main__":
    root = tk.Tk()
    app = OptimizationApp(root)
    root.mainloop()