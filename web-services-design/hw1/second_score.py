n = int(input())
arr = list(map(int, input().split()))

max_score = max(arr)

# убираем все максимальные
filtered = [x for x in arr if x != max_score]

second_max = max(filtered)

print(second_max)
