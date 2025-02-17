import tkinter as tk
from tkinter import messagebox
import random

questions = [
    {
        "question": "Какой язык программирования является основным для разработки веб-сайтов?",
        "options": ["Python", "JavaScript", "Java", "C++"],
        "correct_answer": "JavaScript"
    },
    {
        "question": "Какая планета находится ближе всех к Солнцу?",
        "options": ["Земля", "Меркурий", "Венера", "Марс"],
        "correct_answer": "Меркурий"
    },
    {
        "question": "Какая страна является родиной футбола?",
        "options": ["Бразилия", "Испания", "Италия", "Англия"],
        "correct_answer": "Англия"
    },
    {
        "question": "Как назывался планетарный потрошитель из первой части Dead Space?",
        "options": ["USG Ishimura", "USG O'Bannon", "USG Tereshkova", "USG Clark"],
        "correct_answer": "USG Ishimura"
    },
    {
        "question": "Какой элемент химической таблицы имеет символ 'O'?",
        "options": ["Азот", "Кислород", "Углерод", "Гелий"],
        "correct_answer": "Кислород"
    },
    {
        "question": "Какой элемент таблицы Менделеева имеет атомный номер 1?",
        "options": ["Водород", "Гелий", "Литий", "Кислород"],
        "correct_answer": "Водород"
    },
    {
        "question": "Как называется главный герой игры Dead Space?",
        "options": ["Isaac Clarke", "John Carver", "Markus Tanaka", "David Mercer"],
        "correct_answer": "Isaac Clarke"
    },
    {
        "question": "Что является основной угрозой в Dead Space?",
        "options": ["Зомби", "Некроморфы", "Роботы", "Пираты"],
        "correct_answer": "Некроморфы"
    },
    {
        "question": "Какой океан самый большой по площади?",
        "options": ["Атлантический", "Индийский", "Тихий", "Южный"],
        "correct_answer": "Тихий"
    },
    {
        "question": "Какая страна является крупнейшим производителем кофе?",
        "options": ["Германия", "Италия", "Бразилия", "Колумбия"],
        "correct_answer": "Бразилия"
    },
    {
        "question": "Какое животное является символом Австралии?",
        "options": ["Кенгуру", "Панда", "Тигр", "Лев"],
        "correct_answer": "Кенгуру"
    },
    {
        "question": "Какая река является самой длинной в мире?",
        "options": ["Амазонка", "Нил", "Янцзы", "Миссисипи"],
        "correct_answer": "Амазонка"
    }
]


class QuizApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Викторина")
        self.score = 0
        self.question_index = 0
        random.shuffle(questions)

        self.label_question = tk.Label(root, text="", font=("Arial", 16), wraplength=400)
        self.label_question.pack(pady=20)

        self.buttons = []
        for i in range(4):
            btn = tk.Button(root, text="", font=("Arial", 14), width=30, command=lambda i=i: self.check_answer(i))
            btn.pack(pady=5)
            self.buttons.append(btn)

        self.show_question()

    def show_question(self):
        q = questions[self.question_index]
        self.label_question.config(text=q['question'])
        for i, option in enumerate(q['options']):
            self.buttons[i].config(text=option)

    def check_answer(self, index):
        q = questions[self.question_index]
        selected_answer = self.buttons[index].cget("text")

        if selected_answer == q['correct_answer']:
            self.score += 1
            messagebox.showinfo("Правильно!", "Вы ответили правильно!")
        else:
            messagebox.showinfo("Неправильно", f"Правильный ответ: {q['correct_answer']}")

        self.question_index += 1
        if self.question_index < len(questions):
            self.show_question()
        else:
            self.end_game()

    def end_game(self):
        messagebox.showinfo("Итог", f"Игра окончена! Ваш счет: {self.score} из {len(questions)}")
        self.root.quit()

def main():
    root = tk.Tk()
    app = QuizApp(root)
    root.mainloop()
if __name__ == "__main__":
    main()