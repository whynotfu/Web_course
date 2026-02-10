num1 = int(input())
num2 = int(input())

try:
    print(num1 // num2)
    print(num1 / num2)
except ZeroDivisionError:
    print("division by zero")
