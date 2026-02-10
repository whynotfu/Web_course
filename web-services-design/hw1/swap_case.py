try:
    s = input()
    if not (0 < len(s) <= 1000):
        raise ValueError
except:
    print("ERROR")
    exit()
print(s.swapcase())
