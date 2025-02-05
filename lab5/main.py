import tkinter as tk
import random


class BrownianMotion:
    def __init__(self, root, num_particles=50, width=600, height=400):
        self.root = root
        self.width = width
        self.height = height
        self.particles = []

        # Создаем холст
        self.canvas = tk.Canvas(root, width=width, height=height, bg='white')
        self.canvas.pack()

        # Создаем частицы
        for _ in range(num_particles):
            x = random.randint(0, width)
            y = random.randint(0, height)
            particle = self.canvas.create_oval(
                x - 3, y - 3, x + 3, y + 3, fill='blue'
            )
            self.particles.append({
                'id': particle,
                'dx': random.uniform(-1.5, 1.5),
                'dy': random.uniform(-1.5, 1.5)
            })

        # Запускаем анимацию
        self.animate()

    def check_boundaries(self, pos):
        """Обработка столкновений со стенками"""
        x, y = pos
        new_dx = new_dy = 0

        if x <= 0 or x >= self.width:
            new_dx = -1
        if y <= 0 or y >= self.height:
            new_dy = -1
        return new_dx, new_dy
        return new_dx, new_dy

    def animate(self):
        """Обновление позиций частиц"""
        for particle in self.particles:
            # Получаем текущие координаты
            coords = self.canvas.coords(particle['id'])
            x = (coords[0] + coords[2]) / 2
            y = (coords[1] + coords[3]) / 2

            # Добавляем случайное движение
            particle['dx'] += random.uniform(-0.5, 0.5)
            particle['dy'] += random.uniform(-0.5, 0.5)

            # Ограничиваем максимальную скорость
            particle['dx'] = max(-3, min(3, particle['dx']))
            particle['dy'] = max(-3, min(3, particle['dy']))

            # Рассчитываем новые координаты
            new_x = x + particle['dx']
            new_y = y + particle['dy']

            # Проверяем границы и корректируем движение
            dx_mod, dy_mod = self.check_boundaries((new_x, new_y))
            particle['dx'] *= dx_mod if dx_mod != 0 else 1
            particle['dy'] *= dy_mod if dy_mod != 0 else 1

            # Обновляем позицию
            self.canvas.move(
                particle['id'],
                particle['dx'],
                particle['dy']
            )

        # Повторяем через 30 мс
        self.root.after(30, self.animate)


if __name__ == "__main__":
    root = tk.Tk()
    root.title("Броуновское движение")
    app = BrownianMotion(root)
    root.mainloop()
