number = input("Введите трехзначное число: ").strip()

# Проверка на корректность ввода
if len(number) != 3 or not number.isdigit():
    print("Ошибка: требуется ввести ровно три цифры")
else:
    # Извлекаем цифры
    d1, d2, d3 = map(int, number)

    # Определяем действие по второй цифре
    if 0 <= d2 <= 5:
        result = d2 ** 2
        print(f"Квадрат второй цифры: {result}")
    elif 6 <= d2 <= 7:
        result = d1 + d3
        print(f"Сумма первой и третьей цифр: {result}")
    else:  # 8 или 9
        result = d1 + d2 + d3
        print(f"Сумма всех цифр: {result}")