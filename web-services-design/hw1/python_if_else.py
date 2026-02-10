number = int(input())
if (number%2 != 0):
    print("Weird")
else:
    if (number < 5 and number >1):
        print("Not Weird")
    if (number > 5 and number<=20):
        print("Weird")
    if (number > 20):
         print("Not Weird")