import math
import tkinter as tk
from tkinter import ttk, messagebox


def calculate_circle_metrics(radius):
    """Рассчитывает площадь и длину окружности."""
    area = math.pi * radius ** 2
    circumference = 2 * math.pi * radius
    return area, circumference


def filter_even_above_ten(numbers):
    """Фильтрует четные числа больше 10."""
    try:
        return [num for num in numbers if num % 2 == 0 and num > 10]
    except:
        return []


class CombinedApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Комбинированная программа")
        self.root.geometry("500x600")
        self.root.resizable(False, False)

        # Настройка цветовой схемы
        bg_color = "#f0f0f0"
        button_color = "#4CAF50"
        button_text_color = "white"

        self.root.configure(bg=bg_color)

        # Создаем Notebook (вкладки)
        self.notebook = ttk.Notebook(root)
        self.notebook.pack(fill='both', expand=True)

        # Первая вкладка - калькулятор окружности
        self.create_circle_calculator_tab()

        # Вторая вкладка - фильтр чисел
        self.create_number_filter_tab()

    def create_circle_calculator_tab(self):
        """Создает вкладку калькулятора окружности."""
        tab = ttk.Frame(self.notebook)
        self.notebook.add(tab, text="Калькулятор окружности")

        # Заголовок
        title_label = tk.Label(
            tab,
            text="Калькулятор окружности",
            font=("Arial", 16, "bold"),
            bg="#f0f0f0"
        )
        title_label.pack(pady=20)

        # Фрейм для ввода
        input_frame = tk.Frame(tab, bg="#f0f0f0")
        input_frame.pack(pady=10)

        # Метка и поле для ввода радиуса
        radius_label = tk.Label(
            input_frame,
            text="Радиус окружности:",
            font=("Arial", 12),
            bg="#f0f0f0"
        )
        radius_label.grid(row=0, column=0, padx=10, pady=10)

        self.radius_entry = tk.Entry(input_frame, font=("Arial", 12), width=10)
        self.radius_entry.grid(row=0, column=1, padx=10, pady=10)

        # Кнопка расчета
        calculate_button = tk.Button(
            tab,
            text="Рассчитать",
            font=("Arial", 12),
            bg="#4CAF50",
            fg="white",
            padx=20,
            pady=5,
            command=self.calculate_circle
        )
        calculate_button.pack(pady=15)

        # Фрейм для результатов
        self.circle_result_frame = tk.Frame(tab, bg="#f0f0f0")
        self.circle_result_frame.pack(pady=10)

        # Метки для отображения результатов
        self.area_label = tk.Label(
            self.circle_result_frame,
            text="Площадь: -",
            font=("Arial", 12),
            bg="#f0f0f0"
        )
        self.area_label.pack(pady=5)

        self.circumference_label = tk.Label(
            self.circle_result_frame,
            text="Длина окружности: -",
            font=("Arial", 12),
            bg="#f0f0f0"
        )
        self.circumference_label.pack(pady=5)

        # Привязка клавиши Enter к расчету
        self.radius_entry.bind('<Return>', lambda event: self.calculate_circle())

    def create_number_filter_tab(self):
        """Создает вкладку фильтрации чисел."""
        tab = ttk.Frame(self.notebook)
        self.notebook.add(tab, text="Фильтр чисел")

        # Заголовок
        title_label = tk.Label(
            tab,
            text="Фильтр четных чисел > 10",
            font=("Arial", 16, "bold"),
            bg="#f0f0f0"
        )
        title_label.pack(pady=20)

        # Инструкция
        instruction_label = tk.Label(
            tab,
            text="Введите числа через пробел:",
            font=("Arial", 12),
            bg="#f0f0f0"
        )
        instruction_label.pack(pady=10)

        # Поле для ввода чисел
        self.numbers_entry = tk.Entry(tab, font=("Arial", 12), width=30)
        self.numbers_entry.pack(pady=10)

        # Кнопка фильтрации
        filter_button = tk.Button(
            tab,
            text="Фильтровать",
            font=("Arial", 12),
            bg="#4CAF50",
            fg="white",
            padx=20,
            pady=5,
            command=self.filter_numbers
        )
        filter_button.pack(pady=15)

        # Текстовое поле для вывода результатов
        self.result_text = tk.Text(
            tab,
            height=8,
            width=40,
            font=("Arial", 12),
            state='disabled'
        )
        self.result_text.pack(pady=10)

        # Привязка клавиши Enter к фильтрации
        self.numbers_entry.bind('<Return>', lambda event: self.filter_numbers())

    def calculate_circle(self):
        """Выполняет расчет окружности и обновляет интерфейс."""
        try:
            radius = float(self.radius_entry.get())

            if radius <= 0:
                messagebox.showerror("Ошибка", "Радиус должен быть положительным числом!")
                return

            area, circumference = calculate_circle_metrics(radius)

            # Обновление меток с результатами
            self.area_label.config(text=f"Площадь: {area:.2f}")
            self.circumference_label.config(text=f"Длина окружности: {circumference:.2f}")

        except ValueError:
            messagebox.showerror("Ошибка", "Пожалуйста, введите корректное числовое значение!")

    def filter_numbers(self):
        """Фильтрует числа и выводит результат."""
        input_str = self.numbers_entry.get()

        if not input_str:
            messagebox.showerror("Ошибка", "Пожалуйста, введите числа!")
            return

        try:
            numbers = list(map(int, input_str.split()))
            result = filter_even_above_ten(numbers)

            # Обновление текстового поля
            self.result_text.config(state='normal')
            self.result_text.delete(1.0, tk.END)
            self.result_text.insert(tk.END, f"Исходный список: {numbers}\n\n")
            self.result_text.insert(tk.END, f"Отфильтрованный список (четные > 10): {result}")
            self.result_text.config(state='disabled')

        except ValueError:
            messagebox.showerror("Ошибка", "Пожалуйста, вводите только числа, разделенные пробелами!")


def main():
    root = tk.Tk()
    app = CombinedApp(root)
    root.mainloop()


if __name__ == "__main__":
    main()