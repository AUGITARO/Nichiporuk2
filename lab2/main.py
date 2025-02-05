import tkinter as tk
from tkinter import ttk, messagebox
from PIL import Image, ImageTk
import math


def calculate_Z():
    try:
        k = float(entry_k.get())
        a = float(entry_a.get())
        x = k ** 3 + k + 0.1

        if x >= 0:
            Z = math.sqrt(x ** 2 + a ** 2) + math.sqrt(x / (a + 0.2 * x))
        else:
            Z = -math.sqrt(x ** 2 + a ** 2) - math.sqrt(x / (a + 0.2 * x))

        result_label.config(text=f"Z = {Z:.4f}")
    except Exception as e:
        messagebox.showerror("Ошибка", "Некорректные входные данные")


def calculate_U():
    try:
        x = float(entry_x.get())
        y = float(entry_y.get())

        if function_choice.get() == "sin(x)":
            fx = math.sin(x)
        elif function_choice.get() == "cos(x)":
            fx = math.cos(x)
        else:
            fx = math.exp(x)

        U = fx + y  # Пример формулы, можно заменить

        result_label_U.config(text=f"U = {U:.4f}")
    except Exception as e:
        messagebox.showerror("Ошибка", "Некорректные входные данные")


def open_task1():
    task1_window = tk.Toplevel(root)
    task1_window.title("Вычисление Z")
    task1_window.geometry("500x400")
    task1_window.resizable(False, False)

    global entry_k, entry_a, result_label

    frame = tk.Frame(task1_window)
    frame.pack(expand=True)

    tk.Label(frame, text="Введите k:").pack()
    entry_k = tk.Entry(frame)
    entry_k.pack()

    tk.Label(frame, text="Введите a:").pack()
    entry_a = tk.Entry(frame)
    entry_a.pack()

    tk.Button(frame, text="Вычислить Z", command=calculate_Z).pack()
    result_label = tk.Label(frame, text="")
    result_label.pack()

    try:
        img = Image.open("image.png")
        img = img.resize((300, 100))
        img = ImageTk.PhotoImage(img)
        panel = tk.Label(frame, image=img)
        panel.image = img
        panel.pack()
    except FileNotFoundError:
        tk.Label(frame, text="").pack()


def open_task2():
    task2_window = tk.Toplevel(root)
    task2_window.title("Вычисление U(x, y)")

    global entry_x, entry_y, function_choice, result_label_U

    tk.Label(task2_window, text="Введите x:").pack()
    entry_x = tk.Entry(task2_window)
    entry_x.pack()

    tk.Label(task2_window, text="Введите y:").pack()
    entry_y = tk.Entry(task2_window)
    entry_y.pack()

    function_choice = tk.StringVar(value="sin(x)")
    tk.Radiobutton(task2_window, text="sin(x)", variable=function_choice, value="sin(x)").pack()
    tk.Radiobutton(task2_window, text="cos(x)", variable=function_choice, value="cos(x)").pack()
    tk.Radiobutton(task2_window, text="exp(x)", variable=function_choice, value="exp(x)").pack()

    tk.Button(task2_window, text="Вычислить U", command=calculate_U).pack()
    result_label_U = tk.Label(task2_window, text="")
    result_label_U.pack()


def on_task_selected(event):
    selected_task = task_combobox.get()
    if selected_task == "Задание 1: Вычисление Z":
        open_task1()
    elif selected_task == "Задание 2: Вычисление U(x, y)":
        open_task2()


root = tk.Tk()
root.title("Выбор задания")
root.geometry("300x200")

tk.Label(root, text="Выберите задание:").pack()

task_combobox = ttk.Combobox(root, values=["Задание 1: Вычисление Z", "Задание 2: Вычисление U(x, y)"])
task_combobox.pack()
task_combobox.bind("<<ComboboxSelected>>", on_task_selected)

root.mainloop()
