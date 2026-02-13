def format_phone(number):
    digits = ''.join(c for c in number if c.isdigit())
    if len(digits) == 11:
        digits = digits[1:]
    return f'+7 ({digits[:3]}) {digits[3:6]}-{digits[6:8]}-{digits[8:10]}'

def wrapper(f):
    def fun(l):
        formatted = [format_phone(num) for num in l]
        return f(formatted)
    return fun

@wrapper
def sort_phone(l):
    return sorted(l)

if __name__ == '__main__':
    l = [input() for _ in range(int(input()))]
    print(*sort_phone(l), sep='\n')
