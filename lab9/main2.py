# var 1
def filter_even_above_ten(numbers):
    return [num for num in numbers if num % 2 == 0 and num > 10]

# Ввод списка чисел с клавиатуры
input_str = input("Введите числа через пробел: ")
numbers = list(map(int, input_str.split()))

# Получение и вывод результата
result = filter_even_above_ten(numbers)
print("Отфильтрованный список:", result)