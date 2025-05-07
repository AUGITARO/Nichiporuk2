import tkinter as tk
from tkinter import ttk, messagebox
import numpy as np
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
from matplotlib.figure import Figure
from matplotlib import cm


# Целевая функция
def f(x, y):
    return (1 / (1 + ((x - 2) / 3) ** 2 + ((y - 2) / 3) ** 2) +
            3 / (1 + (x - 1) ** 2 + ((y - 1) / 2) ** 2))


# Градиенты и производные
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


# Метод Гаусса
def gauss_method(start_x, start_y, alpha=0.1, max_iterations=1000, tolerance=1e-6):
    x, y = start_x, start_y
    history = []

    for _ in range(max_iterations):
        current = f(x, y)
        history.append((x, y, current))

        # Поиск по X
        x_step = alpha if f(x + alpha, y) > current else -alpha
        while f(x + x_step, y) > current:
            x += x_step
            current = f(x, y)

        # Поиск по Y
        y_step = alpha if f(x, y + alpha) > current else -alpha
        while f(x, y + y_step) > current:
            y += y_step
            current = f(x, y)

        if abs(current - history[-1][2]) < tolerance:
            break

    return x, y, current, history


# Метод Ньютона
def newton_method(start_x, start_y, max_iterations=100, tolerance=1e-6):
    x, y = start_x, start_y
    history = []

    for _ in range(max_iterations):
        current = f(x, y)
        history.append((x, y, current))

        grad_x = df_dx(x, y)
        grad_y = df_dy(x, y)
        H_xx = d2f_dx2(x, y)
        H_yy = d2f_dy2(x, y)
        H_xy = d2f_dxdy(x, y)

        det = H_xx * H_yy - H_xy ** 2
        if det == 0:
            dx, dy = 0.01 * grad_x, 0.01 * grad_y
        else:
            dx = (H_yy * grad_x - H_xy * grad_y) / det
            dy = (H_xx * grad_y - H_xy * grad_x) / det

        x += dx
        y += dy

        if abs(f(x, y) - current) < tolerance:
            break

    return x, y, f(x, y), history


# GUI класс
class OptimizationApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Optimization Toolkit")
        self.create_widgets()
        self.setup_plots()

    def create_widgets(self):
        control_frame = ttk.Frame(self.root, padding=10)
        control_frame.pack(side=tk.LEFT, fill=tk.Y)

        # Поля ввода
        ttk.Label(control_frame, text="Начальная точка").grid(row=0, columnspan=2)
        ttk.Label(control_frame, text="X:").grid(row=1, column=0)
        self.x_entry = ttk.Entry(control_frame)
        self.x_entry.grid(row=1, column=1)
        self.x_entry.insert(0, "0.0")

        ttk.Label(control_frame, text="Y:").grid(row=2, column=0)
        self.y_entry = ttk.Entry(control_frame)
        self.y_entry.grid(row=2, column=1)
        self.y_entry.insert(0, "0.0")

        # Параметры методов
        ttk.Label(control_frame, text="Метод Гаусса").grid(row=3, columnspan=2, pady=5)
        ttk.Label(control_frame, text="Alpha:").grid(row=4, column=0)
        self.alpha_entry = ttk.Entry(control_frame)
        self.alpha_entry.grid(row=4, column=1)
        self.alpha_entry.insert(0, "0.1")

        ttk.Label(control_frame, text="Max итераций:").grid(row=5, column=0)
        self.gauss_iter_entry = ttk.Entry(control_frame)
        self.gauss_iter_entry.grid(row=5, column=1)
        self.gauss_iter_entry.insert(0, "1000")

        ttk.Label(control_frame, text="Метод Ньютона").grid(row=6, columnspan=2, pady=5)
        ttk.Label(control_frame, text="Max итераций:").grid(row=7, column=0)
        self.newton_iter_entry = ttk.Entry(control_frame)
        self.newton_iter_entry.grid(row=7, column=1)
        self.newton_iter_entry.insert(0, "100")

        # Кнопки
        ttk.Button(control_frame, text="Запустить Гаусса",
                   command=self.run_gauss).grid(row=8, columnspan=2, pady=5)
        ttk.Button(control_frame, text="Запустить Ньютона",
                   command=self.run_newton).grid(row=9, columnspan=2)

        # Область графиков
        self.plot_frame = ttk.Frame(self.root)
        self.plot_frame.pack(side=tk.RIGHT, fill=tk.BOTH, expand=True)

    def setup_plots(self):
        self.fig = Figure(figsize=(10, 8))
        self.canvas = FigureCanvasTkAgg(self.fig, self.plot_frame)
        self.canvas.get_tk_widget().pack(fill=tk.BOTH, expand=True)

    def validate_input(self):
        try:
            float(self.x_entry.get())
            float(self.y_entry.get())
            float(self.alpha_entry.get())
            int(self.gauss_iter_entry.get())
            int(self.newton_iter_entry.get())
            return True
        except ValueError:
            messagebox.showerror("Ошибка", "Некорректные значения параметров")
            return False

    def run_gauss(self):
        if not self.validate_input(): return

        params = {
            'start_x': float(self.x_entry.get()),
            'start_y': float(self.y_entry.get()),
            'alpha': float(self.alpha_entry.get()),
            'max_iterations': int(self.gauss_iter_entry.get())
        }

        x, y, val, hist = gauss_method(**params)
        self.show_results("Гаусс", x, y, val, len(hist))
        self.plot_results(hist, "Метод Гаусса")

    def run_newton(self):
        if not self.validate_input(): return

        params = {
            'start_x': float(self.x_entry.get()),
            'start_y': float(self.y_entry.get()),
            'max_iterations': int(self.newton_iter_entry.get())
        }

        x, y, val, hist = newton_method(**params)
        self.show_results("Ньютон", x, y, val, len(hist))
        self.plot_results(hist, "Метод Ньютона")

    def show_results(self, method, x, y, value, iterations):
        text = (
            f"Метод: {method}\n"
            f"Найденный максимум: ({x:.4f}, {y:.4f})\n"
            f"Значение функции: {value:.4f}\n"
            f"Итераций выполнено: {iterations}"
        )
        messagebox.showinfo("Результаты", text)

    def plot_results(self, history, title):
        self.fig.clf()

        # 3D график
        ax1 = self.fig.add_subplot(121, projection='3d')
        X = np.linspace(-1, 5, 100)
        Y = np.linspace(-1, 5, 100)
        X, Y = np.meshgrid(X, Y)
        Z = np.vectorize(f)(X, Y)
        ax1.plot_surface(X, Y, Z, cmap='viridis', alpha=0.8)
        ax1.set_title(title)

        # Траектория
        path_x = [p[0] for p in history]
        path_y = [p[1] for p in history]
        path_z = [p[2] for p in history]
        ax1.plot(path_x, path_y, path_z, 'r-', lw=2)

        # Контурный график
        ax2 = self.fig.add_subplot(122)
        ax2.contourf(X, Y, Z, levels=50, cmap='viridis')
        ax2.plot(path_x, path_y, 'w--', lw=1.5)
        ax2.set_title("Контурный график")

        self.canvas.draw()


if __name__ == "__main__":
    root = tk.Tk()
    app = OptimizationApp(root)
    root.mainloop()