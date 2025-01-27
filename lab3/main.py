import tkinter as tk

def draw_image(canvas):
    # Фон
    canvas.create_rectangle(0, 0, 800, 600, fill="#AAB7B8", width=0)

    # Прозрачные круги (эффект тумана)
    fog_color = "#9EB1B1"
    canvas.create_oval(100, 100, 500, 400, fill=fog_color, outline="")
    canvas.create_oval(200, 50, 700, 350, fill=fog_color, outline="")
    canvas.create_oval(50, 200, 600, 500, fill=fog_color, outline="")

    # Здания
    buildings = [
        (50, 100, 150, 500, "#7F9999"),
        (120, 50, 220, 450, "#90A5A5"),
        (200, 80, 300, 500, "#A3B6B6"),
        (280, 40, 380, 480, "#6A8989"),
        (700, 70, 780, 500, "#5C7F7F")  # Новое здание справа
    ]

    for x1, y1, x2, y2, color in buildings:
        canvas.create_rectangle(x1, y1, x2, y2, fill=color, width=0)

    # Дорога (нижняя часть)
    canvas.create_oval(-100, 400, 900, 900, fill="#5C6F6F", outline="")

    # Машина
    canvas.create_rectangle(350, 420, 450, 460, fill="#42C5F5", outline="")  # Кузов
    canvas.create_rectangle(380, 410, 420, 430, fill="#9DEDFD", outline="")  # Окна
    canvas.create_rectangle(365, 430, 385, 450, fill="#9DEDFD", outline="")  # Левое окно
    canvas.create_rectangle(415, 430, 435, 450, fill="#9DEDFD", outline="")  # Правое окно
    canvas.create_oval(360, 460, 380, 480, fill="#263737", outline="")  # Левое колесо
    canvas.create_oval(420, 460, 440, 480, fill="#263737", outline="")  # Правое колесо

# Создаем окно
root = tk.Tk()
root.title("Рисунок в Tkinter")

# Настраиваем холст
canvas = tk.Canvas(root, width=800, height=600)
canvas.pack()

# Рисуем изображение
draw_image(canvas)

# Запускаем приложение
root.mainloop()