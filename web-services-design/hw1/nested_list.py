try:
    n = int(input())
    if not (2 <= n <= 5):
        raise ValueError
    students = []
    for _ in range(n):
        name = input().strip()
        score = float(input().strip())
        students.append([name, score])

    scores = sorted(set(score for _, score in students))
    if len(scores) < 2:
        raise ValueError

except:
    print("ERROR")
    exit()

second_lowest = scores[1]
names = sorted(name for name, score in students if score == second_lowest)
for name in names:
    print(name)
