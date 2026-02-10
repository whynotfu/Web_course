n = int(input())

intervals = []

for _ in range(n):
    a, b = map(int, input().split())
    intervals.append((a, b))

T = int(input())

count = 0

for a, b in intervals:
    if a <= T <= b:
        count += 1

print(count)
