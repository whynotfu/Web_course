try:
    a = int(input())
    b = int(input())
    if abs(a) > 10**10 or abs(b) > 10**10:
        raise ValueError
    if b == 0:
        raise ValueError
except:
    print("ERROR")
    exit()
print(a + b)
print(a - b)
print(a * b)
