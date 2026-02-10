import sys

def fail():
    print("ERROR")
    sys.exit(0)

try:
    n_line = input().strip()
    if not n_line:
        fail()
    n = int(n_line)
except Exception:
    fail()

if not (2 <= n <= 10):
    fail()

def read_matrix(n: int):
    mat = []
    for _ in range(n):
        try:
            row = input().split()
        except Exception:
            fail()

        if len(row) != n:
            fail()

        try:
            mat.append([int(x) for x in row])
        except Exception:
            fail()
    return mat

A = read_matrix(n)
B = read_matrix(n)

C = [[0] * n for _ in range(n)]
for i in range(n):
    for j in range(n):
        s = 0
        for k in range(n):
            s += A[i][k] * B[k][j]
        C[i][j] = s

for row in C:
    print(*row)
