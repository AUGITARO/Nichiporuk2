class CoinHandler:
    def __init__(self, denomination, successor=None):
        self.denomination = denomination  # Номинал монеты
        self.successor = successor  # Следующий приемник в цепочке
        self.count = 0  # Счетчик монет данного номинала

    def set_successor(self, successor):
        self.successor = successor

    def handle(self, amount):
        if amount == self.denomination:
            self.count += 1
            print(f"Принята монета {self.denomination} центов.")
        elif self.successor:
            self.successor.handle(amount)

    def get_count(self):
        return self.count

    def get_denomination(self):
        return self.denomination


class CoinAcceptor:
    def __init__(self):
        # Создаем цепочку приемников
        self.one_cent_handler = CoinHandler(1)
        self.five_cent_handler = CoinHandler(5)
        self.ten_cent_handler = CoinHandler(10)
        self.twenty_five_cent_handler = CoinHandler(25)

        # Устанавливаем цепочку
        self.one_cent_handler.set_successor(self.five_cent_handler)
        self.five_cent_handler.set_successor(self.ten_cent_handler)
        self.ten_cent_handler.set_successor(self.twenty_five_cent_handler)

    def accept_coin(self, amount):
        self.one_cent_handler.handle(amount)

    def get_total(self):
        total = (self.one_cent_handler.get_count() * 1 +
                 self.five_cent_handler.get_count() * 5 +
                 self.ten_cent_handler.get_count() * 10 +
                 self.twenty_five_cent_handler.get_count() * 25)
        return total

    def get_summary(self):
        return {
            1: self.one_cent_handler.get_count(),
            5: self.five_cent_handler.get_count(),
            10: self.ten_cent_handler.get_count(),
            25: self.twenty_five_cent_handler.get_count(),
        }


# Пример использования
if __name__ == "__main__":
    acceptor = CoinAcceptor()

    while True:
        try:
            amount = int(input("Введите номинал монеты (1, 5, 10, 25) или 0 для завершения: "))
            if amount == 0:
                break
            elif amount in [1, 5, 10, 25]:
                acceptor.accept_coin(amount)
            else:
                print("Неверный номинал. Пожалуйста, введите 1, 5, 10 или 25.")
        except ValueError:
            print("Пожалуйста, введите целое число.")

    total = acceptor.get_total()
    summary = acceptor.get_summary()

    print("\nОбщая внесенная сумма:", total, "центов")
    print("Количество внесенных монет:")
    for denomination, count in summary.items():
        print(f"{denomination} центов: {count}")