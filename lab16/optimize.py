def input_natural(message):
    while True:
        try:
            value = int(input(message))
            if value > 0:
                return value
            else:
                print("Число должно быть натуральным (больше 0). Попробуйте ещё раз.")
        except ValueError:
            print("Введено не число. Попробуйте ещё раз.")

def input_a(message):
    while True:
        try:
            value = int(input(message))
            if value > 0:
                return value
            else:
                print("Число должно быть натуральным. Попробуйте ещё раз.")
        except ValueError:
            print("Введено не число. Попробуйте ещё раз.")

def is_odd(num):
    return num % 2 != 0

def is_mult3_not5(num):
    return num % 3 == 0 and num % 5 != 0

def is_even_position_and_odd(pos, num):
    return pos % 2 == 0 and is_odd(num)

n = input_natural("Введите количество чисел n: ")
count_a = 0
count_b = 0
count_c = 0

for i in range(n):
    a = input_a(f"Введите число {i + 1}: ")
    pos = i + 1
    if is_odd(a):
        count_a += 1
    if is_mult3_not5(a):
        count_b += 1
    if is_even_position_and_odd(pos, a):
        count_c += 1

print(f"Количество нечётных чисел: {count_a}")
print(f"Количество чисел, кратных 3 и не кратных 5: {count_b}")
print(f"Количество чисел с чётными номерами и нечётных: {count_c}")
