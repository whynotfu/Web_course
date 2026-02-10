try:
    s = input().strip()
    if not (0 < len(s) <= 10**6):
        raise ValueError
    if not all('A' <= c <= 'Z' for c in s):
        raise ValueError

except:
    print("ERROR")
    exit()

vowels = "AEIOU"

kevin = 0
stuart = 0
n = len(s)

for i in range(n):
    if s[i] in vowels:
        kevin += n - i
    else:
        stuart += n - i

if kevin > stuart:
    print(f"Kevin {kevin}")
elif stuart > kevin:
    print(f"Stuart {stuart}")
else:
    print("Draw")
