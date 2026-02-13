import random
import math

def circle_square_mk(r, n):
    inside = 0
    for _ in range(n):
        x = random.uniform(-r, r)
        y = random.uniform(-r, r)
        if x ** 2 + y ** 2 <= r ** 2:
            inside += 1
    return (inside / n) * (2 * r) ** 2

# Погрешность расчёта в зависимости от n (r=10):
# n=100:     погрешность ~10-15%
# n=1000:    погрешность ~3-5%
# n=10000:   погрешность ~1-2%
# n=100000:  погрешность ~0.3-0.5%
# n=1000000: погрешность ~0.1-0.2%
# Погрешность уменьшается пропорционально 1/sqrt(n).

if __name__ == '__main__':
    r = 10
    exact = math.pi * r ** 2
    for n in [100, 1000, 10000, 100000, 1000000]:
        approx = circle_square_mk(r, n)
        error = abs(approx - exact) / exact * 100
        print(f"n={n:>8}: S={approx:.4f}, exact={exact:.4f}, error={error:.2f}%")
