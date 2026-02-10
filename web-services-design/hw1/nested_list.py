students = []

n = int(input())

for _ in range(n):
    name = input()
    score = float(input())
    students.append([name, score])

scores = sorted(set(s for _, s in students))

second_lowest = scores[1]

names = [name for name, score in students if score == second_lowest]

for name in sorted(names):
    print(name)
