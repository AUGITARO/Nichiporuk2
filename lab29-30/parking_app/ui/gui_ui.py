# parking_app/ui/gui_ui.py

import tkinter as tk
from tkinter import ttk, messagebox
from datetime import datetime
from models.car import Car
from services.parking_service import ParkingService
from utils.helpers import validate_numeric_input, format_money, format_time_difference


class ParkingGUI:
    def __init__(self, parking_service: ParkingService):
        self.parking_service = parking_service
        self.root = tk.Tk()
        self.root.title("Управление автостоянкой")
        self.root.geometry("1000x700")

        self.create_widgets()
        self.update_current_cars()
        self.update_history()

    def create_widgets(self):
        # Создаем Notebook (вкладки)
        self.notebook = ttk.Notebook(self.root)
        self.notebook.pack(fill='both', expand=True)

        # Вкладка добавления автомобиля
        self.add_tab = ttk.Frame(self.notebook)
        self.notebook.add(self.add_tab, text='Добавить авто')
        self.create_add_car_tab()

        # Вкладка текущих автомобилей
        self.current_tab = ttk.Frame(self.notebook)
        self.notebook.add(self.current_tab, text='Текущие')
        self.create_current_cars_tab()

        # Вкладка истории
        self.history_tab = ttk.Frame(self.notebook)
        self.notebook.add(self.history_tab, text='История')
        self.create_history_tab()

        # Вкладка поиска
        self.search_tab = ttk.Frame(self.notebook)
        self.notebook.add(self.search_tab, text='Поиск')
        self.create_search_tab()

        # Вкладка статистики
        self.stats_tab = ttk.Frame(self.notebook)
        self.notebook.add(self.stats_tab, text='Статистика')
        self.create_stats_tab()

    def create_add_car_tab(self):
        fields = [
            ('Марка автомобиля', 'car_brand'),
            ('Номер автомобиля', 'car_number'),
            ('ФИО владельца', 'owner_name'),
            ('Скидка (%)', 'discount'),
            ('Почасовая ставка', 'hourly_rate')
        ]

        self.entries = {}
        for i, (label, field) in enumerate(fields):
            lbl = ttk.Label(self.add_tab, text=label)
            lbl.grid(row=i, column=0, padx=10, pady=5, sticky='w')
            entry = ttk.Entry(self.add_tab)
            entry.grid(row=i, column=1, padx=10, pady=5, sticky='ew')
            self.entries[field] = entry

        btn = ttk.Button(self.add_tab, text='Добавить', command=self.add_car)
        btn.grid(row=len(fields), column=0, columnspan=2, pady=10)

    def add_car(self):
        try:
            data = {k: v.get().strip() for k, v in self.entries.items()}
            discount = validate_numeric_input(data['discount'], 0, 100)
            hourly_rate = validate_numeric_input(data['hourly_rate'] or 100, 1)

            car = self.parking_service.add_car(
                car_brand=data['car_brand'],
                car_number=data['car_number'].upper(),
                owner_name=data['owner_name'],
                discount=int(discount),
                hourly_rate=hourly_rate
            )
            messagebox.showinfo("Успех",
                                f"Автомобиль {car.car_brand} {car.car_number} добавлен!\n"
                                f"Время въезда: {car.entry_time.strftime('%d.%m.%Y %H:%M')}")
            self.update_current_cars()
        except Exception as e:
            messagebox.showerror("Ошибка", str(e))

    def create_current_cars_tab(self):
        self.current_tree = ttk.Treeview(self.current_tab, columns=('brand', 'number', 'owner', 'entry', 'cost'),
                                         show='headings')
        self.current_tree.heading('brand', text='Марка')
        self.current_tree.heading('number', text='Номер')
        self.current_tree.heading('owner', text='Владелец')
        self.current_tree.heading('entry', text='Время въезда')
        self.current_tree.heading('cost', text='Текущая стоимость')
        self.current_tree.pack(fill='both', expand=True, padx=10, pady=10)

        remove_frame = ttk.Frame(self.current_tab)
        remove_frame.pack(pady=10)

        ttk.Label(remove_frame, text="Номер авто:").pack(side='left')
        self.remove_number = ttk.Entry(remove_frame, width=15)
        self.remove_number.pack(side='left', padx=5)

        ttk.Button(remove_frame, text='Вывести', command=self.remove_car).pack(side='left')

    def update_current_cars(self):
        for item in self.current_tree.get_children():
            self.current_tree.delete(item)

        for car in self.parking_service.get_current_cars():
            cost = car.calculate_current_cost()
            self.current_tree.insert('', 'end', values=(
                car.car_brand,
                car.car_number,
                car.owner_name,
                car.entry_time.strftime('%d.%m.%Y %H:%M'),
                format_money(cost)
            ))

    def remove_car(self):
        number = self.remove_number.get().strip().upper()
        if not number:
            messagebox.showwarning("Ошибка", "Введите номер автомобиля")
            return

        car, cost = self.parking_service.remove_car(number)
        if not car:
            messagebox.showerror("Ошибка", "Автомобиль не найден")
            return

        msg = (
            f"Автомобиль {car.car_brand} {car.car_number}\n"
            f"Стоимость: {format_money(cost)}\n"
            f"Оплатить сейчас?"
        )
        if messagebox.askyesno("Оплата", msg):
            self.parking_service.pay_for_parking(number)
            messagebox.showinfo("Успех", "Оплачено!")
        else:
            self.parking_service.update_car_debt(number, cost)
            messagebox.showinfo("Информация", f"Задолженность: {format_money(cost)}")

        self.update_current_cars()
        self.update_history()

    def create_history_tab(self):
        self.history_tree = ttk.Treeview(self.history_tab,
                                         columns=('brand', 'number', 'owner', 'entry', 'exit', 'cost', 'status'),
                                         show='headings')

        columns = [
            ('brand', 'Марка'),
            ('number', 'Номер'),
            ('owner', 'Владелец'),
            ('entry', 'Въезд'),
            ('exit', 'Выезд'),
            ('cost', 'Стоимость'),
            ('status', 'Статус')
        ]

        for col, text in columns:
            self.history_tree.heading(col, text=text)
            self.history_tree.column(col, width=100)

        self.history_tree.pack(fill='both', expand=True, padx=10, pady=10)

    def update_history(self):
        for item in self.history_tree.get_children():
            self.history_tree.delete(item)

        for car in self.parking_service.get_parking_history():
            self.history_tree.insert('', 'end', values=(
                car.car_brand,
                car.car_number,
                car.owner_name,
                car.entry_time.strftime('%d.%m.%Y %H:%M'),
                car.exit_time.strftime('%d.%m.%Y %H:%M') if car.exit_time else '',
                format_money(car.cost),
                car.payment_status
            ))

    def create_search_tab(self):
        search_frame = ttk.Frame(self.search_tab)
        search_frame.pack(pady=10)

        ttk.Label(search_frame, text="Поиск:").pack(side='left')
        self.search_entry = ttk.Entry(search_frame, width=30)
        self.search_entry.pack(side='left', padx=5)
        ttk.Button(search_frame, text='Найти', command=self.search_cars).pack(side='left')

        self.search_result = ttk.Treeview(self.search_tab,
                                          columns=('brand', 'number', 'owner', 'status'),
                                          show='headings')

        columns = [
            ('brand', 'Марка'),
            ('number', 'Номер'),
            ('owner', 'Владелец'),
            ('status', 'Статус')
        ]

        for col, text in columns:
            self.search_result.heading(col, text=text)

        self.search_result.pack(fill='both', expand=True, padx=10, pady=10)

    def search_cars(self):
        query = self.search_entry.get().strip()
        if not query:
            return

        for item in self.search_result.get_children():
            self.search_result.delete(item)

        for car in self.parking_service.search_cars(query):
            status = "На стоянке" if not car.exit_time else \
                f"Оплачено: {car.payment_status}"
            self.search_result.insert('', 'end', values=(
                car.car_brand,
                car.car_number,
                car.owner_name,
                status
            ))

    def create_stats_tab(self):
        stats_frame = ttk.Frame(self.stats_tab)
        stats_frame.pack(pady=20)

        self.stats_labels = {
            'current': ttk.Label(stats_frame, text="Авто на стоянке: 0"),
            'total': ttk.Label(stats_frame, text="Всего обслужено: 0"),
            'debtors': ttk.Label(stats_frame, text="Должников: 0"),
            'debt': ttk.Label(stats_frame, text="Общий долг: 0.00 руб.")
        }

        for i, label in enumerate(self.stats_labels.values()):
            label.grid(row=i, column=0, sticky='w', pady=5)

        ttk.Button(stats_frame,
                   text="Обновить",
                   command=self.update_stats).grid(row=4, column=0, pady=10)

        self.update_stats()

    def update_stats(self):
        current = len(self.parking_service.get_current_cars())
        history = len(self.parking_service.get_parking_history())
        debtors = len(self.parking_service.get_debtors())
        total_debt = self.parking_service.get_total_debt()

        self.stats_labels['current'].config(text=f"Авто на стоянке: {current}")
        self.stats_labels['total'].config(text=f"Всего обслужено: {history}")
        self.stats_labels['debtors'].config(text=f"Должников: {debtors}")
        self.stats_labels['debt'].config(text=f"Общий долг: {format_money(total_debt)}")

    def run(self):
        self.root.mainloop()