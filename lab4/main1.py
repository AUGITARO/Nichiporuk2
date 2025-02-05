# Словарь с паролями и соответствующими модулями доступа
access = {
    '9583': ['A', 'B', 'C'],
    '1747': ['A', 'B', 'C'],
    '3331': ['A', 'B'],
    '7922': ['A', 'B'],
    '9455': ['C'],
    '8997': ['C']
}

# Запрос пароля у пользователя
password = input("Введите пароль: ").strip()

# Проверка наличия пароля в системе
if password in access:
    modules = access[password]
    if len(modules) == 1:
        print(f"Доступен модуль базы {modules[0]}")
    else:
        modules_str = ", ".join(modules)
        print(f"Доступны модули базы {modules_str}")
else:
    print("Доступ запрещен")