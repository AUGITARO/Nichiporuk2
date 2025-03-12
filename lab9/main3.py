def process_lists(numbers, params):
    a, b, c = params
    filtered = []
    sum_rest = 0

    for num in numbers:
        if num > a and num < b and num % c == 0:
            filtered.append(num)
        else:
            sum_rest += num

    print("Подходящие элементы:", filtered)
    print("Сумма остальных элементов:", sum_rest)


# Ввод данных
list1 = list(map(int, input("Введите числа первого списка через пробел: ").split()))
list2 = list(map(int, input("Введите три числа a, b, c через пробел: ").split()))

# Проверка корректности ввода
if len(list2) != 3:
    print("Ошибка: нужно ввести ровно три числа для a, b, c")
else:
    process_lists(list1, list2)