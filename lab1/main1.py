import tkinter as tk
from tkinter import ttk, Menu
import math

def update_font():
    # Получаем текущие значения шрифта, цвета и стиля
    font_tuple = (selected_font.get(), 12, selected_style.get())
    color = selected_color.get()

    # Обновляем шрифт и цвет для всех меток и кнопки
    label.config(font=font_tuple, fg=color)
    entry.config(font=font_tuple, fg=color)
    convert_button.config(font=font_tuple, fg=color)

    # Обновляем цвет текста для меток с результатами
    binary_label.config(font=font_tuple, fg=color)
    octal_label.config(font=font_tuple, fg=color)
    hexadecimal_label.config(font=font_tuple, fg=color)

    # Обновляем цвет текста для новых меток с результатами
    binary_input_label.config(font=font_tuple, fg=color)
    binary_to_decimal_label.config(font=font_tuple, fg=color)
    binary_to_octal_label.config(font=font_tuple, fg=color)
    binary_to_hexadecimal_label.config(font=font_tuple, fg=color)

    # Обновляем цвет текста для восьмеричных операций
    octal_a_label.config(font=font_tuple, fg=color)
    octal_b_label.config(font=font_tuple, fg=color)
    octal_sum_label.config(font=font_tuple, fg=color)
    octal_diff_label.config(font=font_tuple, fg=color)

    # Обновляем цвет текста для медианы
    median_a_label.config(font=font_tuple, fg=color)
    median_b_label.config(font=font_tuple, fg=color)
    median_result_label.config(font=font_tuple, fg=color)

def convert_number():
    try:
        decimal_number = int(entry.get())
        binary_number = bin(decimal_number)[2:]  # Преобразуем в двоичную систему
        octal_number = oct(decimal_number)[2:]  # Преобразуем в восьмеричную систему
        hexadecimal_number = hex(decimal_number)[2:].upper()  # Преобразуем в шестнадцатеричную систему

        # Обновляем текст меток с результатами
        binary_label.config(text=f"Двоичная: {binary_number}")
        octal_label.config(text=f"Восьмеричная: {octal_number}")
        hexadecimal_label.config(text=f"Шестнадцатеричная: {hexadecimal_number}")
    except ValueError:
        binary_label.config(text="Ошибка: введите целое число.")
        octal_label.config(text="")
        hexadecimal_label.config(text="")

def convert_binary():
    try:
        binary_number = entry_binary.get()
        decimal_number = int(binary_number, 2)  # Преобразуем из двоичной в десятичную
        octal_number = oct(decimal_number)[2:]  # Преобразуем в восьмеричную систему
        hexadecimal_number = hex(decimal_number)[2:].upper()  # Преобразуем в шестнадцатеричную систему

        # Обновляем текст меток с результатами
        binary_to_decimal_label.config(text=f"Десятичная: {decimal_number}")
        binary_to_octal_label.config(text=f"Восьмеричная: {octal_number}")
        binary_to_hexadecimal_label.config(text=f"Шестнадцатеричная: {hexadecimal_number}")
    except ValueError:
        binary_to_decimal_label.config(text="Ошибка: введите двоичное число.")
        binary_to_octal_label.config(text="")
        binary_to_hexadecimal_label.config(text="")

def convert_octal():
    try:
        a = int(entry_octal_a.get(), 8)  # Преобразуем из восьмеричной в десятичную
        b = int(entry_octal_b.get(), 8)  # Преобразуем из восьмеричной в десятичную
        sum_result = a + b
        diff_result = a - b

        # Обновляем текст меток с результатами
        octal_sum_label.config(text=f"Сумма (a + b): {sum_result}")
        octal_diff_label.config(text=f"Разность (a - b): {diff_result}")
    except ValueError:
        octal_sum_label.config(text="Ошибка: введите корректные восьмеричные числа.")
        octal_diff_label.config(text="")

def calculate_median():
    try:
        a = float(entry_median_a.get())  # Получаем значение катета a
        b = float(entry_median_b.get())  # Получаем значение катета b
        c = math.sqrt(a**2 + b**2)  # Вычисляем длину гипотенузы
        m = 0.5 * math.sqrt(2 * a**2 + 2 * b**2 - c**2)  # Вычисляем длину медианы

        # Обновляем текст метки с результатом
        median_result_label.config(text=f"Длина медианы: {m:.2f}")
    except ValueError:
        median_result_label.config(text="Ошибка: введите корректные значения катетов.")

# Создаем главное окно
root = tk.Tk()
root.title("Конвертер чисел и вычисление медианы")

# Создаем меню
menu = Menu(root)
root.config(menu=menu)

# Создаем подменю для настроек
settings_menu = Menu(menu, tearoff=0)
menu.add_cascade(label="Настройки", menu=settings_menu)

# Выбор шрифта
selected_font = tk.StringVar(value="Arial")
def set_font(font):
    selected_font.set(font)
    update_font()

font_menu = Menu(settings_menu, tearoff=0)
for font in ["Arial", "Courier", "Times New Roman", "Helvetica"]:
    font_menu.add_command(label=font, command=lambda f=font: set_font(f))
settings_menu.add_cascade(label="Шрифт", menu=font_menu)

# Выбор цвета
selected_color = tk.StringVar(value="black")
def set_color(color):
    selected_color.set(color)
    update_font()

color_menu = Menu(settings_menu, tearoff=0)
for color in ["black", "blue ", "green", "red", "purple", "orange"]:
    color_menu.add_command(label=color, command=lambda c=color: set_color(c))
settings_menu.add_cascade(label="Цвет", menu=color_menu)

# Выбор стиля шрифта
selected_style = tk.StringVar(value="normal")
def set_style(style):
    selected_style.set(style)
    update_font()

style_menu = Menu(settings_menu, tearoff=0)
for style in ["normal", "bold", "italic", "bold italic"]:
    style_menu.add_command(label=style, command=lambda s=style: set_style(s))
settings_menu.add_cascade(label="Стиль", menu=style_menu)

# Создаем основной фрейм для размещения элементов
main_frame = tk.Frame(root)
main_frame.pack(pady=10)

# Создаем фрейм для первой колонки
left_frame = tk.Frame(main_frame)
left_frame.pack(side=tk.LEFT, padx=10)

# Создаем текстовые компоненты для десятичного ввода
label = tk.Label(left_frame, text="Введите число в десятичной системе:", font=("Arial", 12))
label.pack(pady=10)

entry = tk.Entry(left_frame, font=("Arial", 12))
entry.pack(pady=10)

convert_button = tk.Button(left_frame, text="Конвертировать", command=convert_number, font=("Arial", 12))
convert_button.pack(pady=10)

# Метки для результатов десятичного ввода
binary_label = tk.Label(left_frame, text="", font=("Arial", 12), fg="blue")
binary_label.pack(pady=5)

octal_label = tk.Label(left_frame, text="", font=("Arial", 12), fg="green")
octal_label.pack(pady=5)

hexadecimal_label = tk.Label(left_frame, text="", font=("Arial", 12), fg="red")
hexadecimal_label.pack(pady=5)

# Создаем текстовые компоненты для двоичного ввода
binary_input_label = tk.Label(left_frame, text="Введите число в двоичной системе:", font=("Arial", 12))
binary_input_label.pack(pady=10)

entry_binary = tk.Entry(left_frame, font=("Arial", 12))
entry_binary.pack(pady=10)

convert_binary_button = tk.Button(left_frame, text="Конвертировать двоичное", command=convert_binary, font=("Arial", 12))
convert_binary_button.pack(pady=10)

# Метки для результатов двоичного ввода
binary_to_decimal_label = tk.Label(left_frame, text="", font=("Arial", 12), fg="blue")
binary_to_decimal_label.pack(pady=5)

binary_to_octal_label = tk.Label(left_frame, text="", font=("Arial", 12), fg="green")
binary_to_octal_label.pack(pady=5)

binary_to_hexadecimal_label = tk.Label(left_frame, text="", font=("Arial", 12), fg="red")
binary_to_hexadecimal_label.pack(pady=5)

# Создаем фрейм для медианы
median_frame = tk.Frame(main_frame)
median_frame.pack(side=tk.LEFT, padx=10)

# Создаем текстовые компоненты для медианы
median_a_label = tk.Label(median_frame, text="Введите катет a:", font=("Arial", 12))
median_a_label.pack(pady=10)

entry_median_a = tk.Entry(median_frame, font=("Arial", 12))
entry_median_a.pack(pady=10)

median_b_label = tk.Label(median_frame, text="Введите катет b:", font=("Arial", 12))
median_b_label.pack(pady=10)

entry_median_b = tk.Entry(median_frame, font=("Arial", 12))
entry_median_b.pack(pady=10)

calculate_median_button = tk.Button(median_frame, text="Вычислить длину медианы", command=calculate_median, font=("Arial", 12))
calculate_median_button.pack(pady=10)

# Метка для результата медианы
median_result_label = tk.Label(median_frame, text="", font=("Arial", 12), fg="blue")
median_result_label.pack(pady=5)

# Создаем текстовые компоненты для восьмеричного ввода
octal_a_label = tk.Label(left_frame, text="Введите число a в восьмеричной системе:", font=("Arial", 12))
octal_a_label.pack(pady=10)

entry_octal_a = tk.Entry(left_frame, font=("Arial", 12))
entry_octal_a.pack(pady=10)

octal_b_label = tk.Label(left_frame, text="Введите число b в восьмеричной системе:", font=("Arial", 12))
octal_b_label.pack(pady=10)

entry_octal_b = tk.Entry(left_frame, font=("Arial", 12))
entry_octal_b.pack(pady=10)

convert_octal_button = tk .Button(left_frame, text="Вычислить a + b и a - b", command=convert_octal, font=("Arial", 12))
convert_octal_button.pack(pady=10)

# Метки для результатов восьмеричного ввода
octal_sum_label = tk.Label(left_frame, text="", font=("Arial", 12), fg="blue")
octal_sum_label.pack(pady=5)

octal_diff_label = tk.Label(left_frame, text="", font=("Arial", 12), fg="green")
octal_diff_label.pack(pady=5)

# Запускаем главный цикл приложения
root.mainloop()