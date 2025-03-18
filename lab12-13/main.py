# Задание 2.1
class TV:
    def __init__(self):
        self.powered_on = False
        self.display_format = "16:9"
        self.brightness = 50
        self.is_3d = False

    def power_on(self):
        self.powered_on = True
        print("Телевизор включен")

    def power_off(self):
        self.powered_on = False
        print("Телевизор выключен")

    def set_display_format(self, format):
        self.display_format = format
        print(f"Установлен формат отображения: {format}")

    def set_brightness(self, level):
        self.brightness = level
        print(f"Яркость установлена на {level}%")

    def enable_3d(self):
        self.is_3d = True
        print("3D режим включен")

    def disable_3d(self):
        self.is_3d = False
        print("3D режим выключен")

class BluRayPlayer:
    def __init__(self):
        self.powered_on = False
        self.playing = False

    def power_on(self):
        self.powered_on = True
        print("Blu-Ray проигрыватель включен")

    def power_off(self):
        self.powered_on = False
        self.playing = False
        print("Blu-Ray проигрыватель выключен")

    def play(self):
        if self.powered_on:
            self.playing = True
            print("Воспроизведение начато")
        else:
            print("Ошибка: проигрыватель выключен")

    def stop(self):
        self.playing = False
        print("Воспроизведение остановлено")

class Receiver:
    def __init__(self):
        self.powered_on = False
        self.volume = 30
        self.sound_mode = "Стерео"

    def power_on(self):
        self.powered_on = True
        print("Ресивер включен")

    def power_off(self):
        self.powered_on = False
        print("Ресивер выключен")

    def set_volume(self, level):
        self.volume = level
        print(f"Громкость установлена на {level}%")

    def set_sound_mode(self, mode):
        self.sound_mode = mode
        print(f"Режим звука: {mode}")

class HomeTheaterFacade:
    def __init__(self):
        self.tv = TV()
        self.bluray = BluRayPlayer()
        self.receiver = Receiver()

    def watch_movie(self):
        print("\nРежим 'Просмотр фильма':")
        self.tv.power_on()
        self.tv.set_display_format("16:9")
        self.tv.set_brightness(70)
        self.tv.enable_3d()
        self.receiver.power_on()
        self.receiver.set_sound_mode("Объемный звук")
        self.receiver.set_volume(50)
        self.bluray.power_on()
        self.bluray.play()

    def listen_to_music(self):
        print("\nРежим 'Прослушивание музыки':")
        self.tv.power_off()
        self.receiver.power_on()
        self.receiver.set_sound_mode("Стерео")
        self.receiver.set_volume(40)
        self.bluray.power_on()
        self.bluray.play()

    def end_session(self):
        print("\nЗавершение сеанса:")
        self.bluray.stop()
        self.bluray.power_off()
        self.receiver.power_off()
        self.tv.power_off()

if __name__ == "__main__":
    home_theater = HomeTheaterFacade()
    print("Выберите режим:")
    print("1 - Просмотр фильма")
    print("2 - Прослушивание музыки")
    choice = input("Введите номер режима: ")
    if choice == "1":
        home_theater.watch_movie()
    elif choice == "2":
        home_theater.listen_to_music()
    else:
        print("Неверный выбор")
    input("\nНажмите Enter для завершения...")
    home_theater.end_session()
