import tkinter as tk
from tkinter import Menu, font


def update_font():
    selected_font = font_var.get()
    selected_size = size_var.get()
    selected_color = color_var.get()
    selected_style = style_var.get()

    # Изменяем стиль шрифта для всех меток и кнопок
    for label in labels:
        label.config(font=(selected_font, selected_size, selected_style), fg=selected_color)

    # Обновляем цвет для кнопки
    calculate_time_button.config(font=(selected_font, selected_size, selected_style), fg=selected_color)


def calculate_time():
    try:
        v = 220  # Скорость в м/с
        l = float(entry_distance.get()) * 1000  # Преобразуем километры в метры
        t = l / v  # Вычисляем время в секундах

        hours = int(t // 3600)  # Часы
        minutes = int((t % 3600) // 60)  # Минуты
        seconds = int(t % 60)  # Секунды

        # Обновляем текст метки с результатом
        time_result_label.config(text=f"Время: {hours} ч, {minutes} мин, {seconds} сек")
    except ValueError:
        time_result_label.config(text="Ошибка: введите корректное расстояние.")


# Создаем главное окно
root = tk.Tk()
root.title("Вычисление времени полета")

# Создаем меню
menu = Menu(root)
root.config(menu=menu)

# Создаем подменю для изменения шрифта
font_menu = Menu(menu, tearoff=0)
menu.add_cascade(label="Шрифт", menu=font_menu)

# Переменные для хранения выбранных значений
font_var = tk.StringVar(value="Arial")
size_var = tk.StringVar(value="12")
color_var = tk.StringVar(value="black")
style_var = tk.StringVar(value="normal")

# Опции шрифтов
fonts = ["Arial", "Helvetica", "Times New Roman"]
sizes = [10, 12, 14, 16, 18, 20]
colors = ["black", "red", "green", "blue"]
styles = ["normal", "bold", "italic", "bold italic"]

# Создаем выпадающие списки для выбора шрифта, размера, цвета и стиля
for font_name in fonts:
    font_menu.add_radiobutton(label=font_name, variable=font_var, command=update_font)

size_menu = Menu(menu, tearoff=0)
menu.add_cascade(label="Размер", menu=size_menu)
for size in sizes:
    size_menu.add_radiobutton(label=str(size), variable=size_var, command=update_font)

color_menu = Menu(menu, tearoff=0)
menu.add_cascade(label="Цвет", menu=color_menu)
for color in colors:
    color_menu.add_radiobutton(label=color, variable=color_var, command=update_font)

style_menu = Menu(menu, tearoff=0)
menu.add_cascade(label="Стиль", menu=style_menu)
for style in styles:
    style_menu.add_radiobutton(label=style, variable=style_var, command=update_font)

# Создаем основной фрейм для размещения элементов
main_frame = tk.Frame(root)
main_frame.pack(pady=10)

# Создаем текстовые компоненты для расчета времени
speed_label = tk.Label(main_frame, text="Введите расстояние в километрах:", font=(font_var.get(), size_var.get()))
speed_label.pack(pady=10)

entry_distance = tk.Entry(main_frame, font=(font_var.get(), size_var.get()))
entry_distance.pack(pady=10)

calculate_time_button = tk.Button(main_frame, text="Вычислить время", command=calculate_time,
                                  font=(font_var.get(), size_var.get()))
calculate_time_button.pack(pady=10)

# Метка для результата времени
time_result_label = tk.Label(main_frame, text="", font=(font_var.get(), size_var.get()), fg=color_var.get())
time_result_label.pack(pady=5)

# Список меток для обновления стиля
labels = [speed_label, time_result_label]

# Запускаем главный цикл приложения
root.mainloop()