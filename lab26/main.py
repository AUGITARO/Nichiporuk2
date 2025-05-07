import tkinter as tk
from tkinter import messagebox


def is_odd(num):
    return num % 2 != 0


def is_mult3_not5(num):
    return num % 3 == 0 and num % 5 != 0


def is_even_position_and_odd(pos, num):
    return pos % 2 == 0 and is_odd(num)


def calculate():
    try:
        # Получение и проверка n
        n = int(entry_n.get())
        if n <= 0:
            raise ValueError("Количество чисел должно быть натуральным (больше 0)")

        # Получение и обработка чисел
        numbers_text = entry_numbers.get()
        if not numbers_text:
            raise ValueError("Введите числа для анализа")

        numbers = list(map(int, numbers_text.split()))
        if len(numbers) != n:
            raise ValueError(f"Нужно ввести ровно {n} чисел")

        # Подсчет характеристик
        count_a = sum(1 for num in numbers if is_odd(num))
        count_b = sum(1 for num in numbers if is_mult3_not5(num))
        count_c = sum(1 for i, num in enumerate(numbers, 1)
                      if is_even_position_and_odd(i, num))

        # Вывод результатов
        result_text = (
            f"Результаты анализа:\n\n"
            f"• Нечётные числа: {count_a}\n"
            f"• Кратные 3 и не кратные 5: {count_b}\n"
            f"• Чётные позиции с нечётными числами: {count_c}"
        )
        label_result.config(text=result_text)

    except ValueError as e:
        messagebox.showerror("Ошибка ввода", str(e))


# Создание графического интерфейса
root = tk.Tk()
root.title("Анализатор чисел")
root.geometry("450x300")
root.resizable(False, False)

# Стилизация
root.configure(bg='#f0f0f0')
font_style = ('Arial', 10)

# Ввод количества чисел
frame_n = tk.Frame(root, bg='#f0f0f0')
frame_n.pack(pady=10)
tk.Label(frame_n, text="Количество чисел (n):", bg='#f0f0f0', font=font_style).pack(side=tk.LEFT, padx=5)
entry_n = tk.Entry(frame_n, width=10, font=font_style)
entry_n.pack(side=tk.LEFT)

# Ввод чисел
frame_numbers = tk.Frame(root, bg='#f0f0f0')
frame_numbers.pack(pady=10)
tk.Label(frame_numbers, text="Числа через пробел:", bg='#f0f0f0', font=font_style).pack(side=tk.LEFT, padx=5)
entry_numbers = tk.Entry(frame_numbers, width=30, font=font_style)
entry_numbers.pack(side=tk.LEFT)

# Кнопка расчета
btn_calculate = tk.Button(root, text="Анализировать", command=calculate,
                          bg='#4CAF50', fg='white', font=font_style, relief=tk.FLAT)
btn_calculate.pack(pady=15)

# Область результатов
label_result = tk.Label(root, text="", justify=tk.LEFT, bg='#f0f0f0',
                        font=font_style, wraplength=400)
label_result.pack()

root.mainloop()