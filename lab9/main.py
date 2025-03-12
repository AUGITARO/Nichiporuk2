import math

def S(r):
    return math.pi * r ** 2

def l(r):
    return 2 * math.pi * r

def krug():
    r = float(input("Введите радиус окружности: "))
    area = S(r)
    circumference = l(r)
    print(f"Площадь: {area}, Длина: {circumference}")

krug()