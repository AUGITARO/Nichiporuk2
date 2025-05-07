import numpy as np
import matplotlib.pyplot as plt
from matplotlib.animation import FuncAnimation
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
import tkinter as tk
from tkinter import ttk, messagebox


class FunctionVisualizationApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Визуализация тригонометрических функций")
        self.root.geometry("1200x800")
        self.root.resizable(True, True)

        # Создание переменных для параметров
        self.cos_amplitude = tk.DoubleVar(value=2.0)
        self.cos_phase = tk.DoubleVar(value=2.0)
        self.sin_amplitude = tk.DoubleVar(value=1.0)
        self.sin_frequency = tk.DoubleVar(value=2.0)
        self.sin_phase = tk.DoubleVar(value=4.0)

        self.t_min = tk.DoubleVar(value=-20 * np.pi)
        self.t_max = tk.DoubleVar(value=10 * np.pi)
        self.t_step = tk.DoubleVar(value=0.1)

        self.animation_speed = tk.IntVar(value=10)
        self.frequencies = [2 * np.pi, 3 * np.pi, 4 * np.pi, 5 * np.pi, 6 * np.pi, 7 * np.pi, 8 * np.pi]

        # Настройка интерфейса
        self.setup_ui()

        # Начальная инициализация данных
        self.calculate_data()

        # Создание графиков
        self.setup_main_graph()

    def setup_ui(self):
        # Основные фреймы
        control_frame = ttk.LabelFrame(self.root, text="Параметры функции")
        control_frame.pack(side=tk.LEFT, fill=tk.Y, padx=10, pady=10)

        graph_frame = ttk.Frame(self.root)
        graph_frame.pack(side=tk.RIGHT, fill=tk.BOTH, expand=True, padx=10, pady=10)

        # Параметры основной функции
        ttk.Label(control_frame, text="Основная функция:", font=('Arial', 12, 'bold')).pack(anchor='w', padx=5, pady=5)
        ttk.Label(control_frame, text="f(t) = A·cos(t-φ₁) + B·sin(ω·t-φ₂)").pack(anchor='w', padx=5)

        param_frame = ttk.Frame(control_frame)
        param_frame.pack(fill=tk.X, padx=5, pady=5)

        # Амплитуда косинуса
        ttk.Label(param_frame, text="A (амплитуда cos):").grid(row=0, column=0, padx=5, pady=5, sticky='w')
        ttk.Spinbox(param_frame, from_=-10, to=10, increment=0.1, textvariable=self.cos_amplitude, width=8).grid(row=0,
                                                                                                                 column=1,
                                                                                                                 padx=5,
                                                                                                                 pady=5)

        # Фаза косинуса
        ttk.Label(param_frame, text="φ₁ (фаза cos):").grid(row=1, column=0, padx=5, pady=5, sticky='w')
        ttk.Spinbox(param_frame, from_=-10, to=10, increment=0.1, textvariable=self.cos_phase, width=8).grid(row=1,
                                                                                                             column=1,
                                                                                                             padx=5,
                                                                                                             pady=5)

        # Амплитуда синуса
        ttk.Label(param_frame, text="B (амплитуда sin):").grid(row=2, column=0, padx=5, pady=5, sticky='w')
        ttk.Spinbox(param_frame, from_=-10, to=10, increment=0.1, textvariable=self.sin_amplitude, width=8).grid(row=2,
                                                                                                                 column=1,
                                                                                                                 padx=5,
                                                                                                                 pady=5)

        # Частота синуса
        ttk.Label(param_frame, text="ω (частота sin):").grid(row=3, column=0, padx=5, pady=5, sticky='w')
        ttk.Spinbox(param_frame, from_=0.1, to=20, increment=0.1, textvariable=self.sin_frequency, width=8).grid(row=3,
                                                                                                                 column=1,
                                                                                                                 padx=5,
                                                                                                                 pady=5)

        # Фаза синуса
        ttk.Label(param_frame, text="φ₂ (фаза sin):").grid(row=4, column=0, padx=5, pady=5, sticky='w')
        ttk.Spinbox(param_frame, from_=-10, to=10, increment=0.1, textvariable=self.sin_phase, width=8).grid(row=4,
                                                                                                             column=1,
                                                                                                             padx=5,
                                                                                                             pady=5)

        # Параметры диапазона времени
        ttk.Separator(control_frame, orient='horizontal').pack(fill=tk.X, padx=5, pady=10)
        ttk.Label(control_frame, text="Параметры времени:", font=('Arial', 12, 'bold')).pack(anchor='w', padx=5, pady=5)

        time_frame = ttk.Frame(control_frame)
        time_frame.pack(fill=tk.X, padx=5, pady=5)

        # Минимальное время
        ttk.Label(time_frame, text="t мин (в π):").grid(row=0, column=0, padx=5, pady=5, sticky='w')
        ttk.Spinbox(time_frame, from_=-100, to=100, increment=1, textvariable=self.t_min, width=8).grid(row=0, column=1,
                                                                                                        padx=5, pady=5)

        # Максимальное время
        ttk.Label(time_frame, text="t макс (в π):").grid(row=1, column=0, padx=5, pady=5, sticky='w')
        ttk.Spinbox(time_frame, from_=-100, to=100, increment=1, textvariable=self.t_max, width=8).grid(row=1, column=1,
                                                                                                        padx=5, pady=5)

        # Шаг времени
        ttk.Label(time_frame, text="Шаг:").grid(row=2, column=0, padx=5, pady=5, sticky='w')
        ttk.Spinbox(time_frame, from_=0.01, to=1, increment=0.01, textvariable=self.t_step, width=8).grid(row=2,
                                                                                                          column=1,
                                                                                                          padx=5,
                                                                                                          pady=5)

        # Скорость анимации
        ttk.Label(time_frame, text="Скорость анимации:").grid(row=3, column=0, padx=5, pady=5, sticky='w')
        ttk.Scale(time_frame, from_=1, to=50, orient='horizontal', variable=self.animation_speed).grid(row=3, column=1,
                                                                                                       padx=5, pady=5,
                                                                                                       sticky='ew')

        # Кнопки управления
        ttk.Separator(control_frame, orient='horizontal').pack(fill=tk.X, padx=5, pady=10)

        button_frame = ttk.Frame(control_frame)
        button_frame.pack(fill=tk.X, padx=5, pady=10)

        ttk.Button(button_frame, text="Применить", command=self.update_graph).pack(side=tk.LEFT, padx=5)
        ttk.Button(button_frame, text="Запустить анимацию", command=self.start_animation).pack(side=tk.LEFT, padx=5)
        ttk.Button(button_frame, text="Синусоиды", command=self.plot_sinusoids).pack(side=tk.LEFT, padx=5)

        # Фрейм для графика
        self.graph_frame = ttk.LabelFrame(graph_frame, text="График функции")
        self.graph_frame.pack(fill=tk.BOTH, expand=True)

    def calculate_data(self):
        """Расчет данных для графика"""
        try:
            # Рассчитываем значения t и y по формуле из параметров
            self.t_values = np.arange(self.t_min.get(), self.t_max.get(), self.t_step.get())
            A = self.cos_amplitude.get()
            phi1 = self.cos_phase.get()
            B = self.sin_amplitude.get()
            omega = self.sin_frequency.get()
            phi2 = self.sin_phase.get()

            self.y_values = A * np.cos(self.t_values - phi1) + B * np.sin(omega * self.t_values - phi2)

            # Данные для синусоид
            self.t_sin = np.linspace(-1, 1, 400)
            self.y_sin_values = [np.sin(f * self.t_sin) for f in self.frequencies]

        except Exception as e:
            messagebox.showerror("Ошибка расчета", f"Произошла ошибка при расчете данных: {str(e)}")

    def setup_main_graph(self):
        """Настройка основного графика"""
        # Очистка фрейма с графиком
        for widget in self.graph_frame.winfo_children():
            widget.destroy()

        # Создание графика
        self.fig, self.ax = plt.subplots(figsize=(10, 6))
        self.line, = self.ax.plot([], [], label=self.get_function_label(), color='purple')
        self.ax.set_xlim(np.min(self.t_values), np.max(self.t_values))
        self.ax.set_ylim(np.min(self.y_values) - 0.5, np.max(self.y_values) + 0.5)
        self.ax.set_title(f'Анимация графика функции {self.get_function_label()}')
        self.ax.set_xlabel('t')
        self.ax.set_ylabel('y(t)')
        self.ax.grid(True)
        self.ax.legend()

        # Размещение графика в tkinter
        canvas = FigureCanvasTkAgg(self.fig, master=self.graph_frame)
        canvas.draw()
        canvas.get_tk_widget().pack(fill=tk.BOTH, expand=True)

    def get_function_label(self):
        """Получение строки с формулой функции для отображения на графике"""
        A = self.cos_amplitude.get()
        phi1 = self.cos_phase.get()
        B = self.sin_amplitude.get()
        omega = self.sin_frequency.get()
        phi2 = self.sin_phase.get()
        return f'${A}\\cos(t-{phi1}) + {B}\\sin({omega}t-{phi2})$'

    def update_graph(self):
        """Обновление графика с новыми параметрами"""
        self.calculate_data()
        self.setup_main_graph()

    def start_animation(self):
        """Запуск анимации"""
        try:
            # Перерасчет данных
            self.calculate_data()
            self.setup_main_graph()

            def update(frame):
                self.line.set_data(self.t_values[:frame], self.y_values[:frame])
                if frame > len(self.t_values) // 3:
                    self.line.set_color('red')
                    if frame > 2 * len(self.t_values) // 3:
                        self.line.set_linewidth(2)
                        self.line.set_color('yellow')
                return self.line,

            self.ani = FuncAnimation(
                self.fig,
                update,
                frames=len(self.t_values),
                interval=self.animation_speed.get(),
                blit=True
            )

            plt.show()
        except Exception as e:
            messagebox.showerror("Ошибка анимации", f"Произошла ошибка при запуске анимации: {str(e)}")

    def plot_sinusoids(self):
        """Отображение графика синусоид с разными частотами"""
        try:
            fig_sinusoids, ax_sinusoids = plt.subplots(figsize=(10, 6))
            for f, y in zip(self.frequencies, self.y_sin_values):
                ax_sinusoids.plot(self.t_sin, y, label=r'$y = \sin(\omega t), \omega = {:.1f}\pi$'.format(f / np.pi))
            ax_sinusoids.set_title('Синусоиды с разными частотами')
            ax_sinusoids.set_xlabel('t')
            ax_sinusoids.set_ylabel('y(t)')
            ax_sinusoids.legend()
            ax_sinusoids.grid(True)
            plt.show()
        except Exception as e:
            messagebox.showerror("Ошибка", f"Произошла ошибка при построении синусоид: {str(e)}")


# Запуск приложения
if __name__ == "__main__":
    root = tk.Tk()
    app = FunctionVisualizationApp(root)
    root.mainloop()