try:
    n = int(input())
    if n < 2:
        raise ValueError
    arr = list(map(int, input().split()))
    if len(arr) != n:
        raise ValueError
    unique_scores = sorted(set(arr))
    if len(unique_scores) < 2:
        raise ValueError
except:
    print("ERROR")
    exit()
second_max = unique_scores[-2]
print(second_max)
