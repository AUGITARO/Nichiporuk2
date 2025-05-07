import numpy as np

def quadratic(x1, x2):
    return 100*(x2 - x1)**2 + (1 - x1)**2

def rosenbrock(x1, x2):
    return 100*(x2 - x1**2)**2 + (1 - x1)**2

def custom_func(x, y):
    return (1/(1 + ((x-2)/3)**2 + ((y-2)/3)**2) +
           3/(1 + (x-1)**2 + ((y-1)/2)**2))

def compute_gradient(func, x, y, h=1e-5):
    dx = (func(x+h, y) - func(x-h, y)) / (2*h)
    dy = (func(x, y+h) - func(x, y-h)) / (2*h)
    return dx, dy

def optimize(func, start_points, lr=0.001, max_iter=1000):
    results = []
    for x0, y0 in start_points:
        x, y = x0, y0
        for _ in range(max_iter):
            grad_x, grad_y = compute_gradient(func, x, y)
            x -= lr * grad_x
            y -= lr * grad_y
        results.append((x, y, func(x, y)))
    return results

# Исследование всех функций
functions = [quadratic, rosenbrock, custom_func]
start_points = [(0,0), (2,2), (3,3)]

for idx, func in enumerate(functions, 1):
    res = optimize(func, start_points[:2] if idx <3 else start_points[1:])
    print(f"\nФункция {idx}:")
    for (x, y, val), point in zip(res, start_points):
        print(f"Старт {point} -> ({x:.4f}, {y:.4f}), f={val:.4f}")
