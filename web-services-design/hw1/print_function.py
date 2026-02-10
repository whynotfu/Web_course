try:
    n = int(input())

    if not (1 <= n <= 20):
        raise ValueError
except:
    print("ERROR")
    exit()
for i in range(1, n + 1):
    print(i, end="")
