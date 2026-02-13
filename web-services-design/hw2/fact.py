import sys

sys.setrecursionlimit(200000)


def fact_rec(n):
    if not isinstance(n, int) or isinstance(n, bool):
        raise TypeError("n must be an integer")
    if n < 1 or n > 100000:
        raise ValueError("n must be between 1 and 100000")
    if n == 1:
        return 1
    return n * fact_rec(n - 1)


def fact_it(n):
    if not isinstance(n, int) or isinstance(n, bool):
        raise TypeError("n must be an integer")
    if n < 1 or n > 100000:
        raise ValueError("n must be between 1 and 100000")
    result = 1
    for i in range(2, n + 1):
        result *= i
    return result


# Сравнение скорости:
# Для n=1000:  fact_it ~0.001 с, fact_rec ~0.002 с
# Для n=10000: fact_it ~0.07 с,  fact_rec ~0.15 с
# Итерационная версия стабильно быстрее рекурсивной примерно в 1.5-2 раза
# за счёт отсутствия накладных расходов на вызовы функций.
# Рекурсивная версия также ограничена глубиной стека (требует sys.setrecursionlimit).

if __name__ == '__main__':
    import timeit

    for n in [10, 100, 1000, 10000]:
        t_rec = timeit.timeit(lambda: fact_rec(n), number=10)
        t_it = timeit.timeit(lambda: fact_it(n), number=10)
        print(f"n={n}: fact_rec={t_rec:.6f}s, fact_it={t_it:.6f}s")
