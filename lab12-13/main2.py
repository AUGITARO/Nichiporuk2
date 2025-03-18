# задание 3.1
from abc import ABC, abstractmethod

class Component(ABC):
    @abstractmethod
    def add(self, component):
        pass

    @abstractmethod
    def remove(self, component):
        pass

    @abstractmethod
    def get_staff_list(self):
        pass

    @abstractmethod
    def get_total_positions(self):
        pass

    @abstractmethod
    def get_total_salary(self):
        pass

class Position:
    def __init__(self, name, count, salary):
        self.name = name
        self.count = count
        self.salary = salary

class Department(Component):
    def __init__(self, code, name):
        self.code = code
        self.name = name
        self.children = []
        self.positions = []

    def add(self, component):
        self.children.append(component)

    def remove(self, component):
        self.children.remove(component)

    def add_position(self, position):
        self.positions.append(position)

    def remove_position(self, position_name):
        self.positions = [p for p in self.positions if p.name != position_name]

    def get_staff_list(self):
        staff = []
        staff.extend(self.positions)
        for child in self.children:
            staff.extend(child.get_staff_list())
        return staff

    def get_total_positions(self):
        total = sum(p.count for p in self.positions)
        for child in self.children:
            total += child.get_total_positions()
        return total

    def get_total_salary(self):
        total = sum(p.count * p.salary for p in self.positions)
        for child in self.children:
            total += child.get_total_salary()
        return total

if __name__ == "__main__":
    root = Department("001", "Главный офис")
    it_dept = Department("002", "IT отдел")
    hr_dept = Department("003", "HR отдел")

    root.add(it_dept)
    root.add(hr_dept)

    it_dept.add_position(Position("Разработчик", 5, 100000))
    it_dept.add_position(Position("Тестировщик", 3, 80000))

    hr_dept.add_position(Position("Рекрутер", 2, 60000))
    hr_dept.add_position(Position("Менеджер по кадрам", 1, 90000))

    dev_group = Department("004", "Группа разработки")
    it_dept.add(dev_group)
    dev_group.add_position(Position("Старший разработчик", 2, 150000))

    print("Штатное расписание главного офиса:")
    for pos in root.get_staff_list():
        print(f"{pos.name}: {pos.count} ставок, оклад {pos.salary}")

    print(f"\nВсего ставок: {root.get_total_positions()}")
    print(f"Суммарный оклад: {root.get_total_salary()}")