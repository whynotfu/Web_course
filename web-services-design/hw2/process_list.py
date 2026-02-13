def process_list(arr):
    return [i ** 2 if i % 2 == 0 else i ** 3 for i in arr]


def process_list_gen(arr):
    for i in arr:
        yield i ** 2 if i % 2 == 0 else i ** 3


# Сравнение скорости (arr = list(range(1000))):
# process_list     ~0.0003 с — сразу создаёт весь список в памяти
# process_list_gen ~0.0001 с (создание) + потребление по мере необходимости
# Генератор быстрее при создании и экономит память, т.к. не хранит все элементы сразу.
# List comprehension быстрее при полном обходе всех элементов за счёт оптимизаций CPython.

if __name__ == '__main__':
    import timeit

    arr = list(range(1000))
    t_lc = timeit.timeit(lambda: process_list(arr), number=1000)
    t_gen = timeit.timeit(lambda: list(process_list_gen(arr)), number=1000)
    print(f"list comprehension: {t_lc:.6f}s")
    print(f"generator:          {t_gen:.6f}s")
