import numpy as np
import matplotlib.pyplot as plt
from matplotlib.animation import FuncAnimation

t_values = np.arange(-20 * np.pi, 10 * np.pi, 0.1)
y_values = 2 * np.cos(t_values - 2) + np.sin(2 * t_values - 4)

t_sin = np.linspace(-1, 1, 400)
frequencies = [2 * np.pi, 3 * np.pi, 4 * np.pi, 5 * np.pi, 6 * np.pi, 7 * np.pi, 8 * np.pi]
y_sin_values = [np.sin(f * t_sin) for f in frequencies]
fig, ax = plt.subplots(figsize=(10, 6))
line, = ax.plot([], [], label=r'$2\cos(t-2) + \sin(2t-4)$', color='purple')
ax.set_xlim(np.min(t_values), np.max(t_values))
ax.set_ylim(np.min(y_values), np.max(y_values))
ax.set_title(r'Анимация графика функции $2\cos(t-2) + \sin(2t-4)$')
ax.set_xlabel('t')
ax.set_ylabel('y(t)')
ax.grid(True)

def plot_sinusoids():
    fig_sinusoids, ax_sinusoids = plt.subplots(figsize=(10, 6))
    for f, y in zip(frequencies, y_sin_values):
        ax_sinusoids.plot(t_sin, y, label=r'$y = \sin(\omega t), \omega = {:.1f}\pi$'.format(f / np.pi))
    ax_sinusoids.set_title('Синусоиды с разными частотами')
    ax_sinusoids.set_xlabel('t')
    ax_sinusoids.set_ylabel('y(t)')
    ax_sinusoids.legend()
    ax_sinusoids.grid(True)
    plt.show()

def update(frame):
    line.set_data(t_values[:frame], y_values[:frame])
    if frame > len(t_values) // 3:
        line.set_color('red')
        if frame > 2 * len(t_values) // 3:
            line.set_linewidth(2)
            line.set_color('yellow')
    return line,
ani = FuncAnimation(fig, update, frames=len(t_values), interval=10, blit=True)
plt.show()
plot_sinusoids()