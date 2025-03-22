from abc import ABC, abstractmethod

# Продукт (отчет)
class Report:
    def __init__(self, student_name):
        self.student_name = student_name
        self.sections = []

    def add_section(self, title, content):
        self.sections.append(f"<h2>{title}</h2>\n<p>{content}</p>")

    def generate_html(self):
        html_content = f"<html><body><h1>Отчет студента {self.student_name}</h1>"
        html_content += "".join(self.sections) + "</body></html>"
        return html_content


# Абстрактный строитель
class ReportBuilder(ABC):
    @abstractmethod
    def add_title(self, title): pass

    @abstractmethod
    def add_section(self, title, content): pass

    @abstractmethod
    def get_report(self): pass


# Конкретный строитель для HTML
class HTMLReportBuilder(ReportBuilder):
    def __init__(self, student_name):
        self.report = Report(student_name)

    def add_title(self, title):
        self.report.add_section("Титульный лист", f"<h1>{title}</h1>")

    def add_section(self, title, content):
        self.report.add_section(title, content)

    def get_report(self):
        return self.report


# Директор (управляет построением отчета)
class ReportDirector:
    def __init__(self, builder: ReportBuilder):
        self.builder = builder

    def construct_report(self, discipline, experiment_desc, results, analysis, conclusion, grades):
        self.builder.add_title(f"Отчет по дисциплине {discipline}")
        self.builder.add_section("Цель работы", "Изучить работу с HTML-отчетами.")
        self.builder.add_section("Задание", "Формирование отчета с учетом особенностей дисциплины.")
        self.builder.add_section("Теоретические сведения", '''Порождающие шаблоны (creationalpatterns) – 
        шаблоны проектирования, которые абстрагируют процесс наследования. Они позволяют сделать систему независимой от 
        способа создания, композиции и представления объектов. Шаблон, порождающий классы, использует наследование, 
        чтобы изменять наследуемый класс, а шаблон, порождающий объекты, делегирует наследование другому объекту.
        Эти шаблоны оказываются важны, когда система больше зависит от композиции объектов, чем от наследования классов. 
        Получается так, что основной упор делается не на жестком кодировании фиксированного набора поведений, 
        а на определении небольшого набора фундаментальных поведений, с помощью композиции которых можно получать любое 
        число более сложных. Таким образом, для создания объектов с конкретным поведением требуется нечто большее, 
        чем простое инстанцирование класса. Порождающие шаблоны инкапсулируют знания о конкретных классах, которые 
        применяются в системе. Они скрывают детали того, как эти классы создаются и стыкуются. Единственная информация 
        об объектах, известная системе, – это их интерфейсы, определенные с помощью абстрактных классов. 
        Следовательно, порождающие шаблоны обеспечивают большую гибкость при решении вопроса о том, что создается, 
        кто это создает, как и когда. Можно собрать систему из «готовых» объектов с самой различной структурой и 
        функциональностью статически (на этапе компиляции) или динамически (во время выполнения). Иногда допустимо 
        выбирать между тем или иным порождающим шаблоном. Например, есть случаи, когда с пользой для дела можно 
        использовать как прототип, так и абстрактную фабрику. В других ситуациях порождающие шаблоны дополняют друг 
        друга. Так, применяя строитель, можно использовать другие шаблоны для решения вопроса о том, какие компоненты 
        нужно строить, а прототип часто реализуется вместе с одиночкой. Порождающие шаблоны тесно связаны друг с другом, 
        их рассмотрение лучше проводить совместно, чтобы лучше были видны их сходства и различия''')
        self.builder.add_section("Описание экспериментальной установки", experiment_desc)
        self.builder.add_section("Результаты работы", results)
        self.builder.add_section("Анализ результатов работы", analysis)
        self.builder.add_section("Выводы", conclusion)

        grades_html = "<table border='1'><tr><th>Дисциплина</th>"
        for i in range(1, 7):
            grades_html += f"<th>Лб {i}</th>"
        grades_html += "</tr>"

        for subject, marks in grades.items():
            grades_html += f"<tr><td>{subject}</td>"
            for mark in marks:
                grades_html += f"<td>{mark}</td>"
            grades_html += "</tr>"
        grades_html += "</table>"

        self.builder.add_section("Оценки по лабораторным работам", grades_html)

    def get_report(self):
        return self.builder.get_report()


# Клиентский код
if __name__ == "__main__":
    student_name = input("Введите ФИО студента: ")
    builder = HTMLReportBuilder(student_name)
    director = ReportDirector(builder)

    disciplines = ["Базы данных", "Компьютерные сети", "Программирование"]
    grades = {}
    for discipline in disciplines:
        marks = []
        for i in range(1, 7):
            mark = input(f"Введите оценку за Лб {i} по {discipline}: ")
            marks.append(mark)
        grades[discipline] = marks

    experiment_desc = "Использование паттерна Строитель для генерации отчета."
    results = "Пример HTML-отчета с разделами."
    analysis = "Шаблон позволяет гибко формировать структуру отчета."
    conclusion = "Строитель удобен для пошагового создания сложных документов."

    director.construct_report("ИТ-специальности", experiment_desc, results, analysis, conclusion, grades)
    report = director.get_report()

    with open("report.html", "w", encoding="utf-8") as file:
        file.write(report.generate_html())

    print("Отчет сформирован: report.html")