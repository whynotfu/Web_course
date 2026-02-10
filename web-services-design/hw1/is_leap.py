try:
    year_input = input().strip()
    year = int(year_input)
    if not (1900 <= year <= 10**5):
        raise ValueError

except:
    print("ERROR")
    exit()

def is_leap(y):
    if y % 400 == 0:
        return True
    if y % 100 == 0:
        return False
    if y % 4 == 0:
        return True
    return False

print(is_leap(year))
