def compute_average_scores(scores):
    return tuple(sum(student_scores) / len(student_scores) for student_scores in zip(*scores))

if __name__ == '__main__':
    n, x = map(int, input().split())
    scores = []
    for _ in range(x):
        scores.append(tuple(map(float, input().split())))
    averages = compute_average_scores(scores)
    for avg in averages:
        print(avg)
