# happiness.py

try:
    parts = input().split()
    if len(parts) != 2:
        raise ValueError

    n, m = map(int, parts)

    if not (1 <= n <= 10**5 and 1 <= m <= 10**5):
        raise ValueError

    arr = list(map(int, input().split()))
    A = set(map(int, input().split()))
    B = set(map(int, input().split()))

    if len(arr) != n or len(A) != m or len(B) != m:
        raise ValueError

    for x in arr:
        if not (1 <= x <= 10**9):
            raise ValueError

except:
    print("ERROR")
    exit()

# --- логика после успешной валидации ---

happiness = 0

for x in arr:
    if x in A:
        happiness += 1
    elif x in B:
        happiness -= 1

print(happiness)
