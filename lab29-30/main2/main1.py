import tkinter as tk
from tkinter import ttk, messagebox
from datetime import datetime
from parking_app import (
    cars_data, save_data, calculate_cost,
    add_car as original_add_car,
    remove_car as original_remove_car,
    show_current_cars as original_show_current_cars,
    show_history as original_show_history,
    search_car as original_search_car,
    pay_debt as original_pay_debt,
    show_debtors as original_show_debtors
)


class ParkingAppGUI:
    def __init__(self, root):
        self.root = root
        self.root.title("Управление автостоянкой")

        # Стиль для кнопок
        style = ttk.Style()
        style.configure('TButton', padding=5, font=('Arial', 10))

        # Создание кнопок
        buttons = [
            ("Добавить автомобиль", self.open_add_car),
            ("Вывести автомобиль", self.open_remove_car),
            ("Текущие автомобили", self.show_current),
            ("История стоянки", self.show_history),
            ("Поиск автомобиля", self.open_search),
            ("Оплата задолженности", self.open_pay_debt),
            ("Список должников", self.show_debtors),
            ("Выход", self.root.quit)
        ]

        for text, command in buttons:
            btn = ttk.Button(root, text=text, command=command)
            btn.pack(fill=tk.X, padx=5, pady=2)

    def open_add_car(self):
        window = tk.Toplevel(self.root)
        window.title("Добавить автомобиль")

        fields = [
            ("Марка автомобиля", "brand"),
            ("Номер автомобиля", "number"),
            ("ФИО владельца", "owner"),
            ("Скидка (%)", "discount")
        ]

        entries = {}
        for i, (label, name) in enumerate(fields):
            tk.Label(window, text=label).grid(row=i, column=0, padx=5, pady=5)
            entry = ttk.Entry(window)
            entry.grid(row=i, column=1, padx=5, pady=5)
            entries[name] = entry

        def submit():
            try:
                discount = int(entries['discount'].get())
                if not (0 <= discount <= 100):
                    raise ValueError
            except ValueError:
                messagebox.showerror("Ошибка", "Скидка должна быть числом от 0 до 100")
                return

            result = original_add_car(
                entries['brand'].get(),
                entries['number'].get(),
                entries['owner'].get(),
                discount
            )
            messagebox.showinfo("Результат", result)
            window.destroy()

        ttk.Button(window, text="Добавить", command=submit).grid(row=4, columnspan=2, pady=10)

    def open_remove_car(self):
        window = tk.Toplevel(self.root)
        window.title("Вывести автомобиль")

        ttk.Label(window, text="Номер автомобиля:").pack(padx=10, pady=5)
        number_entry = ttk.Entry(window)
        number_entry.pack(padx=10, pady=5)

        def submit():
            car_number = number_entry.get()
            car = next((c for c in cars_data if c['car_number'] == car_number and not c['exit_time']), None)

            if not car:
                messagebox.showerror("Ошибка", "Автомобиль не найден")
                window.destroy()
                return

            exit_time = datetime.now()
            entry_time = datetime.fromisoformat(str(car['entry_time'])) if isinstance(car['entry_time'], str) else car[
                'entry_time']
            cost = calculate_cost(
                entry_time,
                exit_time,
                car['hourly_rate'],
                car['discount']
            )

            car['exit_time'] = exit_time
            car['debt'] = cost
            car['payment_status'] = 'Не оплачено'
            save_data()

            if messagebox.askyesno("Оплата", f"Стоимость: {cost:.2f} руб.\nОплатить сейчас?"):
                car['payment_status'] = 'Оплачено'
                car['debt'] = 0.0
                save_data()
                messagebox.showinfo("Успех", "Оплачено успешно")
            else:
                messagebox.showinfo("Информация", f"Задолженность: {cost:.2f} руб.")

            window.destroy()

        ttk.Button(window, text="Вывести", command=submit).pack(pady=10)

    def show_current(self):
        window = tk.Toplevel(self.root)
        window.title("Текущие автомобили")

        tree = ttk.Treeview(window, columns=("brand", "number", "owner", "entry_time", "cost"), show="headings")
        tree.heading("brand", text="Марка")
        tree.heading("number", text="Номер")
        tree.heading("owner", text="Владелец")
        tree.heading("entry_time", text="Время въезда")
        tree.heading("cost", text="Текущая стоимость")

        for car in cars_data:
            if not car['exit_time']:
                entry_time = datetime.fromisoformat(str(car['entry_time'])) if isinstance(car['entry_time'], str) else \
                car['entry_time']
                now = datetime.now()
                cost = calculate_cost(entry_time, now, car['hourly_rate'], car['discount'])
                tree.insert("", "end", values=(
                    car['car_brand'],
                    car['car_number'],
                    car['owner_name'],
                    entry_time.strftime("%d.%m.%Y %H:%M"),
                    f"{cost:.2f} руб."
                ))

        tree.pack(fill=tk.BOTH, expand=True)
        ttk.Scrollbar(window, orient=tk.VERTICAL, command=tree.yview).pack(side=tk.RIGHT, fill=tk.Y)
        tree.configure(yscrollcommand=lambda *args: None)

    def show_history(self):
        window = tk.Toplevel(self.root)
        window.title("История стоянки")

        tree = ttk.Treeview(window, columns=("brand", "number", "entry", "exit", "cost", "status"), show="headings")
        tree.heading("brand", text="Марка")
        tree.heading("number", text="Номер")
        tree.heading("entry", text="Въезд")
        tree.heading("exit", text="Выезд")
        tree.heading("cost", text="Стоимость")
        tree.heading("status", text="Статус")

        for car in cars_data:
            if car['exit_time']:
                entry = datetime.fromisoformat(str(car['entry_time'])) if isinstance(car['entry_time'], str) else car[
                    'entry_time']
                exit = datetime.fromisoformat(str(car['exit_time'])) if isinstance(car['exit_time'], str) else car[
                    'exit_time']
                tree.insert("", "end", values=(
                    car['car_brand'],
                    car['car_number'],
                    entry.strftime("%d.%m.%Y %H:%M"),
                    exit.strftime("%d.%m.%Y %H:%M"),
                    f"{car.get('cost', 0):.2f} руб.",
                    car['payment_status']
                ))

        tree.pack(fill=tk.BOTH, expand=True)
        ttk.Scrollbar(window, orient=tk.VERTICAL, command=tree.yview).pack(side=tk.RIGHT, fill=tk.Y)
        tree.configure(yscrollcommand=lambda *args: None)

    def open_search(self):
        window = tk.Toplevel(self.root)
        window.title("Поиск автомобиля")

        ttk.Label(window, text="Поиск (номер/марка/владелец):").pack(padx=10, pady=5)
        search_entry = ttk.Entry(window)
        search_entry.pack(padx=10, pady=5)

        tree = ttk.Treeview(window, columns=("brand", "number", "owner", "status"), show="headings")
        tree.heading("brand", text="Марка")
        tree.heading("number", text="Номер")
        tree.heading("owner", text="Владелец")
        tree.heading("status", text="Статус")
        tree.pack(fill=tk.BOTH, expand=True)

        def search():
            term = search_entry.get().lower()
            tree.delete(*tree.get_children())
            for car in cars_data:
                if (term in car['car_number'].lower() or
                        term in car['car_brand'].lower() or
                        term in car['owner_name'].lower()):
                    status = "На стоянке" if not car['exit_time'] else "Уехал"
                    tree.insert("", "end", values=(
                        car['car_brand'],
                        car['car_number'],
                        car['owner_name'],
                        status
                    ))

        ttk.Button(window, text="Искать", command=search).pack(pady=10)

    def open_pay_debt(self):
        window = tk.Toplevel(self.root)
        window.title("Оплата задолженности")

        ttk.Label(window, text="Номер автомобиля:").pack(padx=10, pady=5)
        number_entry = ttk.Entry(window)
        number_entry.pack(padx=10, pady=5)

        def submit():
            car_number = number_entry.get()
            car = next((c for c in cars_data if c['car_number'] == car_number and c['debt'] > 0), None)

            if not car:
                messagebox.showinfo("Информация", "Нет задолженности")
                window.destroy()
                return

            car['payment_status'] = 'Оплачено'
            car['debt'] = 0.0
            save_data()
            messagebox.showinfo("Успех", "Задолженность погашена")
            window.destroy()

        ttk.Button(window, text="Оплатить", command=submit).pack(pady=10)

    def show_debtors(self):
        debtors = [c for c in cars_data if c['payment_status'] == 'Не оплачено' and c['debt'] > 0]

        window = tk.Toplevel(self.root)
        window.title("Список должников")

        if not debtors:
            ttk.Label(window, text="Должников нет").pack(padx=10, pady=10)
            return

        total = sum(c['debt'] for c in debtors)
        ttk.Label(window, text=f"Общая задолженность: {total:.2f} руб.").pack()

        tree = ttk.Treeview(window, columns=("number", "owner", "debt"), show="headings")
        tree.heading("number", text="Номер")
        tree.heading("owner", text="Владелец")
        tree.heading("debt", text="Задолженность")

        for car in debtors:
            tree.insert("", "end", values=(car['car_number'], car['owner_name'], f"{car['debt']:.2f} руб."))

        tree.pack(fill=tk.BOTH, expand=True)


def add_car(brand, number, owner, discount):
    try:
        discount = int(discount)
        if not (0 <= discount <= 100):
            return "Скидка должна быть от 0 до 100%"
    except ValueError:
        return "Неверный формат скидки"

    car = {
        "car_brand": brand,
        "car_number": number,
        "owner_name": owner,
        "entry_time": datetime.now(),
        "hourly_rate": 100,
        "discount": discount,
        "exit_time": None,
        "payment_status": "Не оплачено",
        "debt": 0.0
    }
    cars_data.append(car)
    save_data()
    return f"Автомобиль {brand} {number} добавлен"


if __name__ == "__main__":
    root = tk.Tk()
    app = ParkingAppGUI(root)
    root.mainloop()