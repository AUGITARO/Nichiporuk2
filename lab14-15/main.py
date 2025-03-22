# 1.1

import tkinter as tk
from tkinter import messagebox


class HelpHandler:
    def __init__(self, successor=None):
        self._successor = successor

    def handle_request(self, widget):
        if self._successor:
            return self._successor.handle_request(widget)
        return None


class ButtonHandler(HelpHandler):
    def handle_request(self, widget):
        if isinstance(widget, tk.Button):
            return "Кнопка: Нажмите для выполнения действия."
        return super().handle_request(widget)


class EntryHandler(HelpHandler):
    def handle_request(self, widget):
        if isinstance(widget, tk.Entry):
            return "Текстовое поле: Введите текст."
        return super().handle_request(widget)


class WindowHandler(HelpHandler):
    def handle_request(self, widget):
        if isinstance(widget, tk.Tk):
            return "Главное окно: Основной интерфейс приложения."
        return super().handle_request(widget)


class Application:
    def __init__(self, root):
        self.root = root
        self.root.title("Справка")

        self.button = tk.Button(root, text="Печать")
        self.button.pack(pady=10)

        self.entry = tk.Entry(root)
        self.entry.pack(pady=10)

        self.menu = tk.Menu(root, tearoff=0)
        self.menu.add_command(label="?", command=self.show_help)

        self.root.bind("<Button-3>", self.show_menu)

        self.chain = ButtonHandler(EntryHandler(WindowHandler()))

    def show_menu(self, event):
        self.menu.post(event.x_root, event.y_root)

    def show_help(self):
        widget = self.root.focus_get()
        help_text = self.chain.handle_request(widget)
        messagebox.showinfo("Справка", help_text if help_text else "Справка отсутствует.")


if __name__ == "__main__":
    root = tk.Tk()
    app = Application(root)
    root.mainloop()